import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_viva_document(output_path="CampusNav_Viva_Comprehensive_Notes.docx"):
    doc = docx.Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)
        section.different_first_page_header_footer = True
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("CampusNav • NSUT Smart Campus Navigation & Resource Optimizer")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("NSUT Dwarka • Department of Computer Science & Engineering • Viva Examination Notes")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)

    # Color Palette
    COLOR_PRIMARY = RGBColor(30, 58, 138)     # Deep Navy (#1E3A8A)
    COLOR_SECONDARY = RGBColor(2, 132, 199)   # Vibrant Blue / Cyan (#0284C7)
    COLOR_TEXT = RGBColor(15, 23, 42)         # Slate 900 (#0F172A)
    COLOR_MUTED = RGBColor(71, 85, 105)       # Slate 600 (#475569)
    COLOR_EMERALD = RGBColor(5, 150, 105)     # Success / Emerald (#059669)
    COLOR_PURPLE = RGBColor(126, 34, 206)     # Deep Purple (#7E22CE)

    def set_cell_background(cell, fill_hex):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for margin_name, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
            node = parse_xml(f'<{margin_name} {nsdecls("w")} w:w="{val}" w:type="dxa"/>')
            tcMar.append(node)
        tcPr.append(tcMar)

    def add_title(text, subtitle=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(2)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(24)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY

        if subtitle:
            p2 = doc.add_paragraph()
            p2.paragraph_format.space_before = Pt(2)
            p2.paragraph_format.space_after = Pt(16)
            p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run2 = p2.add_run(subtitle)
            run2.font.name = "Calibri"
            run2.font.size = Pt(12)
            run2.font.italic = True
            run2.font.color.rgb = COLOR_SECONDARY

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = COLOR_TEXT
        return p

    def add_body(text, bold_prefix=None, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = "Calibri"
            r_bold.font.size = Pt(10)
            r_bold.font.bold = True
            r_bold.font.color.rgb = COLOR_TEXT
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10)
        run.font.color.rgb = COLOR_TEXT
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = "Calibri"
            r_bold.font.size = Pt(10)
            r_bold.font.bold = True
            r_bold.font.color.rgb = COLOR_TEXT
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10)
        run.font.color.rgb = COLOR_TEXT
        return p

    def add_callout(text, title="KEY VIVA INSIGHT"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.8)
        set_cell_background(cell, "F0F9FF") # Light cyan/blue
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="0284C7"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        cp = cell.paragraphs[0]
        cp.paragraph_format.space_after = Pt(2)
        r_title = cp.add_run(f"★ {title}: ")
        r_title.font.name = "Arial"
        r_title.font.size = Pt(10)
        r_title.font.bold = True
        r_title.font.color.rgb = COLOR_SECONDARY

        r_text = cp.add_run(text)
        r_text.font.name = "Calibri"
        r_text.font.size = Pt(9.5)
        r_text.font.color.rgb = COLOR_TEXT
        
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(4)
        p_after.paragraph_format.space_after = Pt(2)

    # =========================================================================
    # DOCUMENT COVER & HEADER
    # =========================================================================
    add_title("CampusNav: Smart Campus Navigation & Resource Optimizer", 
              "Comprehensive Theoretical & Practical Notes for Project Viva Voce Examination")

    # Metadata Box
    meta_tbl = doc.add_table(rows=2, cols=3)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_headers = ["Institution", "Domain", "Key Concepts"]
    meta_values = [
        "Netaji Subhas University of Technology (NSUT)", 
        "Geospatial Graph Theory & Web Systems", 
        "Dijkstra, A*, BFS, DFS, Kruskal/Prim MST, DP Knapsack"
    ]
    for c_idx in range(3):
        c_hdr = meta_tbl.cell(0, c_idx)
        c_val = meta_tbl.cell(1, c_idx)
        set_cell_background(c_hdr, "1E3A8A")
        set_cell_background(c_val, "F8FAFC")
        set_cell_margins(c_hdr, top=80, bottom=80, left=100, right=100)
        set_cell_margins(c_val, top=80, bottom=80, left=100, right=100)
        
        p0 = c_hdr.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r0 = p0.add_run(meta_headers[c_idx])
        r0.font.bold = True
        r0.font.size = Pt(9)
        r0.font.color.rgb = RGBColor(255, 255, 255)

        p1 = c_val.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p1.add_run(meta_values[c_idx])
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = COLOR_TEXT

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_after = Pt(8)

    # =========================================================================
    # SECTION 1: EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # =========================================================================
    add_heading_1("1. Project Overview & Motivation")
    add_body(
        "CampusNav is an enterprise-grade, high-performance web navigation and resource optimization system designed "
        "specifically for the 145-acre campus of Netaji Subhas University of Technology (NSUT), Dwarka, New Delhi. "
        "Modern university campuses present unique geospatial navigation hurdles: labyrinthine academic blocks, multi-floor "
        "indoor breezeways, pedestrian-only plazas, restricted service roads, and temporary event closures. Commercial mapping "
        "services (such as Google Maps) typically optimize for vehicular roads and fail to accurately model pedestrian footpaths, "
        "accessible wheelchair routes, indoor hallway crossings, or campus-specific facility infrastructure."
    )
    add_body(
        "CampusNav solves these challenges by combining rigorous Graph Theory, Classic Data Structures, Geodesic Mathematics, "
        "and Dynamic Programming into an intuitive, responsive Single Page Application (SPA)."
    )

    add_heading_2("Key Objectives Accomplished:")
    add_bullet(" To map all 145 acres of NSUT into an exact mathematical graph G = (V, E) based on real-world OpenStreetMap (OSM) satellite data.", "Mathematical Graph Representation:")
    add_bullet(" Implementing Dijkstra's Algorithm and A* Search with custom Min-Heaps for sub-millisecond route calculation.", "Optimal Pedestrian Routing:")
    add_bullet(" Modeling special indoor connections through Admin Block ground floor, Block 6 central lobby, and the Block 5-to-Library breezeway gate to Training & Placement (TnP).", "Indoor Walkways & Breezeways:")
    add_bullet(" Dynamic filtering of stairs and steep steps for wheelchair users with 100% ramp-compliant paths.", "Accessible Routing:")
    add_bullet(" Fiber-optic network and utility pipeline optimization using Kruskal's and Prim's Minimum Spanning Tree (MST) algorithms.", "Campus Infrastructure Optimization:")
    add_bullet(" Optimal non-conflicting event slot allocation in high-demand campus venues (Auditorium, APJ Complex, Moksha Ground) using Weighted Interval Scheduling Dynamic Programming.", "Resource Scheduling:")
    add_bullet(" HTML5 Geolocation API integration, live nearest-node snapping, turn-by-turn cardinal instructions, and walk simulation.", "Real-Time Tracking & User Experience:")

    # =========================================================================
    # SECTION 2: PROJECT ARCHITECTURE (EXAMINER-FOCUSED)
    # =========================================================================
    add_heading_1("2. Project Architecture & System Design")
    
    add_callout(
        "\"CampusNav follows a Decoupled 4-Tier Client-Side Architecture. The Presentation Layer (HTML5/CSS3/Leaflet.js) handles UI "
        "interactions and map rendering. When a user selects a destination, the Controller Layer (app.js) captures the event, retrieves GPS "
        "coordinates, and snaps them to the nearest node in our Topological Graph Layer (graphData.js, 1,409 nodes, 1,564 edges). "
        "It then calls the Algorithmic Engine (algorithms.js), which executes Dijkstra or A* using a custom Binary Min-Heap in sub-millisecond time. "
        "The calculated path and bearing angles are returned to the controller to render the animated route polyline and turn-by-turn guidance. "
        "Because the entire engine runs on the client side with zero backend latency, routing is instantaneous and works even offline.\"",
        "30-SECOND ELEVATOR PITCH FOR YOUR PROFESSOR"
    )

    add_heading_2("2.1 High-Level 4-Tier Architecture Diagram")
    add_body(
        "The system is organized into four distinct, loosely coupled architectural layers with clean separation of concerns:"
    )

    # Architecture Table Diagram
    arch_tbl = doc.add_table(rows=5, cols=3)
    arch_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    arch_headers = ["Layer / Tier", "Key Modules & Files", "Responsibilities & Core Functions"]
    arch_tiers = [
        ["Tier 1:\nPresentation &\nVisualization", 
         "• index.html\n• styles.css\n• leaflet.js (v1.9.4)\n• leaflet.css", 
         "• Interactive dual-tile Leaflet canvas (Carto Voyager street & Esri Satellite).\n• Glassmorphic floating navigation control panel & search bars.\n• Clean location name pill badges & interactive marker pins.\n• Animated path polylines, direction arrows & simulation walker marker."],
        
        ["Tier 2:\nApplication Controller\n& State Machine", 
         "• app.js\n• HTML5 Geolocation API\n• Event Listeners", 
         "• User event orchestration (origin/destination picks, algorithm switching).\n• Real-time GPS coordinate acquisition via watchPosition.\n• Spatial Snapping: queries graph to map user coordinates to nearest vertex.\n• Dynamic route rerouting, obstacle handling & environmental multipliers.\n• Turn-by-turn instruction synthesizer & walk simulation timer."],
        
        ["Tier 3:\nAlgorithmic & Data\nStructures Engine", 
         "• algorithms.js\n• Binary Min-Heap\n• Disjoint Set Union (DSU)", 
         "• Custom Binary Min-Heap Priority Queue: O(log V) push/pop operations.\n• Disjoint Set Union (DSU) with Path Compression & Union-by-Rank: O(α(n)).\n• Shortest Path Algorithms: Dijkstra, A* (Haversine heuristic), BFS, DFS.\n• Network Spanning: Kruskal's & Prim's Minimum Spanning Tree (MST).\n• Resource Scheduling: DP Weighted Interval Scheduling (O(n log n))."],
        
        ["Tier 4:\nGeospatial Graph\nData & Topology", 
         "• graphData.js\n• Raw OSM Overpass Feed\n• Hand-curated POI DB", 
         "• Topological Graph G = (V, E) of NSUT: |V| = 1,409 nodes, |E| = 1,564 edges.\n• GeoJSON node attributes: WGS-84 coordinates, junction IDs, types.\n• Edge attributes: weight in meters, highway tag, wheelchair accessibility flag.\n• 28 Landmark POIs across 7 categories (Academic, Hostels, Admin, etc.).\n• Indoor Breezeway & Corridor subgraphs (Admin Block, Block 6, Library gate)."]
    ]

    for c_i, h_text in enumerate(arch_headers):
        c = arch_tbl.cell(0, c_i)
        set_cell_background(c, "1E3A8A")
        set_cell_margins(c, top=80, bottom=80, left=90, right=90)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_i, r_data in enumerate(arch_tiers):
        for c_i, val in enumerate(r_data):
            c = arch_tbl.cell(r_i + 1, c_i)
            bg = "F0F9FF" if r_i % 2 == 1 else "FFFFFF"
            set_cell_background(c, bg)
            set_cell_margins(c, top=70, bottom=70, left=90, right=90)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_i == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_PRIMARY

    p_spacer_arch = doc.add_paragraph()
    p_spacer_arch.paragraph_format.space_after = Pt(8)

    add_heading_2("2.2 Request-Response Execution Flow (Step-by-Step)")
    add_body(
        "To explain the runtime behavior during a viva, walk through this 5-step lifecycle when a user clicks 'Find Route':"
    )
    add_bullet(
        "The user selects an origin (e.g. 'Main Gate') and a destination (e.g. 'APJ Complex') or enables 'Use My Current Location'. "
        "The UI fires an event listener in app.js.",
        "Step 1: Input & Geolocation Capture: "
    )
    add_bullet(
        "app.js retrieves the coordinates. If arbitrary GPS coordinates are given, the Spatial Snapping Algorithm scans graphData.js "
        "using Haversine distance minimization to locate the nearest walkable junction node V_start and V_end.",
        "Step 2: Spatial Snapping: "
    )
    add_bullet(
        "app.js invokes findShortestPath(startNodeId, endNodeId, options) in algorithms.js. "
        "Depending on the selected mode (Dijkstra or A*), the algorithm pops vertices from the custom Min-Heap, evaluates neighboring edges "
        "subject to accessibility and weather filters, relaxes distance costs, and reaches the goal.",
        "Step 3: Graph Traversal & Heuristic Search: "
    )
    add_bullet(
        "The path is reconstructed via the prev predecessor map. For every consecutive node pair, the initial geodetic forward bearing θ is calculated. "
        "Angular changes are classified into human-readable instructions: 'Turn sharp left heading toward Moksha Ground', 'Continue straight for 45m', etc.",
        "Step 4: Path Backtracking & Turn-by-Turn Synthesis: "
    )
    add_bullet(
        "The ordered coordinate array is returned to app.js, which clears previous map layers, renders a glowing polyline onto the Leaflet canvas, "
        "zooms to fit the route bounds, populates the turn-by-turn panel, and initiates the animated walker cursor.",
        "Step 5: Vector Polyline & UI Rendering: "
    )

    add_heading_2("2.3 Key Architectural Strengths to Highlight in Viva")
    add_bullet(
        "Eliminates network round-trip delays, API rate-limiting, and server hosting expenses. Route calculations execute in under 2 milliseconds directly in the browser V8 engine.",
        "Zero Backend Dependency (Pure Client-Side Edge Execution): "
    )
    add_bullet(
        "The complete graph of 1,409 nodes and 1,564 edges occupies only ~1.6 MB in JavaScript memory, easily running on low-end budget smartphones.",
        "Minimal Memory Footprint: "
    )
    add_bullet(
        "The presentation UI is completely separated from graph traversal logic. Swapping Leaflet for MapLibre or Google Maps requires modifying only the rendering layer without touching algorithms.js.",
        "Modular Decoupled Design: "
    )
    add_bullet(
        "Because all graph data and algorithms are bundled locally, the entire navigation system can function without an active internet connection once loaded as a PWA (Progressive Web App).",
        "Offline-Ready Resilience: "
    )

    # =========================================================================
    # SECTION 3: METHODOLOGY & DATA EXTRACTION
    # =========================================================================
    add_heading_1("3. Methodology & Geospatial Data Pipeline")
    add_body(
        "The project follows a rigorous end-to-end engineering pipeline from raw satellite data extraction to browser visualization:"
    )

    add_heading_2("Stage 1: Geospatial Extraction & Boundary Clipping")
    add_body(
        "Raw geospatial data for the bounding box [28.6040, 77.0315] to [28.6160, 77.0440] was ingested using the OpenStreetMap (OSM) Overpass API. "
        "Overpass nodes and ways were filtered by highway tags: footway, path, pedestrian, service, steps, and living_street. "
        "Vehicular perimeter highways outside the campus security boundary were isolated to prevent routes spilling onto public roads."
    )

    add_heading_2("Stage 2: Graph Extraction & Connectivity Verification")
    add_body(
        "A graph connectivity audit was performed using Breadth-First Search (BFS) to identify connected components. Any disconnected island nodes "
        "were pruned or manually linked to ensure a single, strongly connected graph. The final campus graph consists of:"
    )
    add_bullet("1,409 distinct walkable junction nodes with latitude and longitude in WGS-84 coordinate system.", "|V| = ")
    add_bullet("1,564 bidirectional pedestrian edges, each tagged with distance in meters, highway type, and accessibility attributes.", "|E| = ")
    add_bullet("28 curated campus facilities across Academic, Hostels, Admin, Food, Sports, Gates, Landmarks, and Utility categories.", "Landmarks = ")

    add_heading_2("Stage 3: Spatial Snapping Algorithm")
    add_body(
        "Users and physical landmarks rarely coincide with an exact surveyed footpath vertex. To connect arbitrary coordinates (such as the user's live GPS position) "
        "to the walking network, CampusNav applies a Spatial Snapping Algorithm:"
    )
    add_bullet(
        "Given coordinate P = (lat_p, lon_p), compute HaversineDistance(P, V_i) for all V_i in V. "
        "Identify the node V_snap = argmin HaversineDistance(P, V_i). "
        "The system creates an implicit virtual connector link from P to V_snap, incorporating the lead-in walking distance.",
        "Nearest Node Snapping Formulation: "
    )

    add_callout(
        "In a viva, if asked how GPS inaccuracy is handled: Explain that the HTML5 Geolocation API returns a coordinate with an accuracy circle (in meters). "
        "CampusNav checks if the coordinate falls within the NSUT campus boundary polygon. If inside, it projects the position onto the nearest walkable graph node V_snap. "
        "This prevents the user marker from jumping onto grass lawns or inside solid walls.",
        "EXAMINER DEFENSE: GPS NOISE & SNAPPING"
    )

    # =========================================================================
    # SECTION 4: MATHEMATICAL FORMULATIONS
    # =========================================================================
    add_heading_1("4. Core Mathematical Formulations")
    
    add_heading_2("4.1 Haversine Great-Circle Distance Formula")
    add_body(
        "Because Euclidean distance (sqrt(dx^2 + dy^2)) assumes a flat Euclidean plane, it introduces massive geometric distortion on spherical planetary surfaces. "
        "CampusNav calculates all edge weights and heuristic distances using the Haversine Formula over the WGS-84 Earth sphere:"
    )
    add_body("Let latitude and longitude of two points be (φ1, λ1) and (φ2, λ2) in radians. Let R = 6,371,000 meters (mean Earth radius).", bold_prefix="Variables: ")
    add_body("Δφ = φ2 - φ1,    Δλ = λ2 - λ1", bold_prefix="Angular Differences: ")
    add_body("a = sin²(Δφ / 2) + cos(φ1) · cos(φ2) · sin²(Δλ / 2)", bold_prefix="Haversine Term (a): ")
    add_body("c = 2 · atan2( √a, √(1 - a) )", bold_prefix="Angular Distance (c): ")
    add_body("Distance (d) = R · c   (meters)", bold_prefix="Final Ground Distance: ")

    add_heading_2("4.2 Initial Geodetic Bearing (Turn-by-Turn Navigation)")
    add_body(
        "To calculate direction of travel (e.g. 'Turn sharp left heading North-East') between consecutive waypoints P1 and P2, the forward azimuth bearing θ is computed:"
    )
    add_body("y = sin(Δλ) · cos(φ2)", bold_prefix="y-component: ")
    add_body("x = cos(φ1) · sin(φ2) - sin(φ1) · cos(φ2) · cos(Δλ)", bold_prefix="x-component: ")
    add_body("θ = (atan2(y, x) · 180 / π + 360) mod 360", bold_prefix="Bearing Angle (θ): ")
    add_body(
        "The angular difference (turnAngle = (bearing_curr - bearing_prev + 540) mod 360 - 180) determines whether the pedestrian is instructed to turn "
        "left, slight left, right, sharp right, or continue straight."
    )

    # =========================================================================
    # SECTION 5: DATA STRUCTURES
    # =========================================================================
    add_heading_1("5. Fundamental Data Structures Implemented")
    
    add_heading_2("5.1 Custom Binary Min-Heap Priority Queue")
    add_body(
        "Dijkstra's and Prim's algorithms require repeatedly extracting the minimum-distance vertex. A naive linear scan yields O(V) per extraction (O(V^2) total). "
        "CampusNav implements an in-memory Binary Min-Heap where each node satisfies: parent.priority <= children.priority."
    )
    add_bullet("Insert element at end of array, bubble up while element.priority < parent.priority. Time Complexity: O(log V).", "Push (Bubble-Up): ")
    add_bullet("Replace root with last element, sink down by swapping with smaller child. Time Complexity: O(log V).", "Pop (Sink-Down): ")
    add_bullet("Check root element. Time Complexity: O(1).", "Peek / IsEmpty: ")

    add_heading_2("5.2 Disjoint Set Union (DSU / Union-Find)")
    add_body(
        "Kruskal's MST algorithm requires detecting whether two vertices belong to the same connected component in near-constant time to avoid cycles. "
        "CampusNav implements DSU with two crucial optimizations:"
    )
    add_bullet(
        "During find(i), we recursively attach the node directly to the set representative root: parent[i] = find(parent[i]). "
        "This flattens the tree structure so subsequent lookups execute in O(1).",
        "Path Compression: "
    )
    add_bullet(
        "When uniting two trees, the root of the smaller rank tree is attached under the root of the larger rank tree. "
        "Rank only increments if both trees have identical rank.",
        "Union by Rank: "
    )
    add_callout(
        "With Path Compression and Union by Rank, any sequence of m operations on n elements executes in O(m · α(n)) time, "
        "where α is the inverse Ackermann function. In practice, α(n) <= 4 for all realistic values of n (even 10^80), "
        "making operations effectively O(1) amortized!",
        "THEORETICAL PROOF: DSU COMPLEXITY"
    )

    add_heading_2("5.3 Graph Adjacency List")
    add_body(
        "The graph is stored as an Adjacency List (Hash Map where key = nodeId, value = Array of Edge objects). "
        "Space Complexity is O(V + E). In contrast, an Adjacency Matrix would require O(V^2) space (~1,409^2 = 1.98 million entries), "
        "wasting memory since the pedestrian network is sparse (average degree ≈ 2.22 edges per node)."
    )

    # =========================================================================
    # SECTION 6: ROUTING ALGORITHMS
    # =========================================================================
    add_heading_1("6. In-Depth Routing Algorithms & Comparison")
    
    add_heading_2("6.1 Dijkstra's Algorithm (Min-Heap Priority Queue)")
    add_body(
        "Dijkstra's algorithm finds the shortest path from a starting node to all other nodes in a weighted graph with non-negative edge weights. "
        "CampusNav uses an early-exit optimization: as soon as the destination vertex u == endNode is popped from the priority queue, the algorithm terminates."
    )
    add_bullet("dist[v] = Infinity for all v, dist[startNode] = 0. MinHeap.push(startNode, 0).", "Initialization: ")
    add_bullet("Pop vertex u with smallest dist[u]. If already visited, continue. Mark visited[u] = true.", "Relaxation Step: ")
    add_bullet(
        "For each neighbor v of u with edge weight w: alt = dist[u] + w. "
        "If alt < dist[v], then dist[v] = alt, prev[v] = u, MinHeap.push(v, alt).",
        "Edge Update: "
    )
    add_bullet("Time: O((V + E) log V). Space: O(V).", "Complexity: ")

    add_heading_2("6.2 A* (A-Star) Search Algorithm")
    add_body(
        "A* enhances Dijkstra by directing search toward the goal using a heuristic evaluation function: f(n) = g(n) + h(n)."
    )
    add_bullet("The exact accumulated distance from the starting node to current node n.", "g(n) [Path Cost]: ")
    add_bullet("The estimated great-circle Haversine distance from node n to the destination node.", "h(n) [Heuristic Estimate]: ")
    add_bullet("The estimated total cost of the path passing through node n.", "f(n) [Priority]: ")
    add_bullet(
        "A heuristic is admissible if it never overestimates the true cost to reach the goal: h(n) <= h*(n). "
        "Because the great-circle Haversine distance is the shortest possible physical distance between two spherical points, "
        "the actual walking distance along physical pathways can never be less than the Haversine distance. "
        "Therefore, our heuristic is 100% admissible, guaranteeing that A* returns the mathematically optimal shortest path!",
        "Proof of Admissibility: "
    )
    add_bullet("Time: O((V + E) log V) in worst-case; in practice visits 80% fewer nodes than Dijkstra. Space: O(V).", "Complexity: ")

    add_heading_2("6.3 Breadth-First Search (BFS) - Unweighted Fewest Hops")
    add_body(
        "BFS explores vertices level by level using a FIFO Queue. It treats all edges as having uniform weight (1 hop). "
        "BFS minimizes the total number of turns/intersections rather than physical metric meters. Useful for campus visitors seeking the simplest route with fewer path transitions."
    )
    add_bullet("Time: O(V + E). Space: O(V).", "Complexity: ")

    add_heading_2("6.4 Depth-First Search (DFS) - Deep Path Exploration")
    add_body(
        "DFS explores as deeply as possible along each branch before backtracking, using a LIFO Stack. "
        "In our application, DFS serves as an educational benchmark: it illustrates how unguided traversal produces convoluted, highly suboptimal paths "
        "(e.g., 2,624 meters vs Dijkstra's 661 meters)."
    )
    add_bullet("Time: O(V + E). Space: O(V).", "Complexity: ")

    # Table: Algorithm Comparison
    add_heading_3("Algorithm Benchmark Comparison on NSUT Graph (Main Gate → APJ Complex):")
    algo_tbl = doc.add_table(rows=5, cols=6)
    algo_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Algorithm", "Distance (m)", "Nodes Visited", "Time (ms)", "Optimality", "Primary Use Case"]
    rows_data = [
        ["Dijkstra", "661 m", "610 nodes", "4.2 ms", "100% Guaranteed", "Standard optimal ground routing"],
        ["A* Search", "661 m", "122 nodes", "0.8 ms", "100% Guaranteed", "Fastest goal-directed routing (5x speedup)"],
        ["BFS", "690 m", "835 nodes", "1.9 ms", "Hop-Optimal", "Routes with minimum turns/junctions"],
        ["DFS", "2,624 m", "452 nodes", "1.1 ms", "Suboptimal", "Educational demonstration of backtracking"]
    ]
    for c_i, h_text in enumerate(headers):
        c = algo_tbl.cell(0, c_i)
        set_cell_background(c, "1E3A8A")
        set_cell_margins(c, top=80, bottom=80, left=80, right=80)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_i, r_data in enumerate(rows_data):
        for c_i, val in enumerate(r_data):
            c = algo_tbl.cell(r_i + 1, c_i)
            bg = "F0F9FF" if r_i == 1 else ("FFFFFF" if r_i % 2 == 0 else "F8FAFC")
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i in [1, 2, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if r_i == 1 and c_i == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_SECONDARY

    p_spacer2 = doc.add_paragraph()
    p_spacer2.paragraph_format.space_after = Pt(8)

    # =========================================================================
    # SECTION 7: NETWORK OPTIMIZATION (MST)
    # =========================================================================
    add_heading_1("7. Campus Infrastructure Optimization (Minimum Spanning Tree)")
    add_body(
        "Beyond individual pedestrian navigation, campus administrators face infrastructure layout challenges: connecting all 28 major landmarks "
        "with high-speed fiber-optic network cables, water distribution pipes, or security CCTV lines with the minimum total trenching and cabling cost. "
        "A Spanning Tree connects all V vertices using exactly V - 1 edges with zero cycles. The Minimum Spanning Tree (MST) minimizes the sum of edge weights."
    )

    add_heading_2("7.1 Kruskal's Algorithm (Edge-Centric)")
    add_bullet("Compute pairwise shortest walking distance between all landmark pairs using Dijkstra's algorithm.", "Step 1: ")
    add_bullet("Sort all candidate edges in non-decreasing order of weight. Time: O(E log E).", "Step 2: ")
    add_bullet("Iterate through sorted edges. For edge (u, v), check DSU.find(u) == DSU.find(v).", "Step 3: ")
    add_bullet("If different sets, add edge to MST and call DSU.union(u, v). If same set, discard (prevents cycles).", "Step 4: ")
    add_bullet("Stop when exactly |V_landmarks| - 1 edges have been added.", "Step 5: ")
    add_bullet("Total NSUT Fiber-Optic Cable Length: 3,569 meters across 26 tree links connecting all landmarks.", "NSUT Result: ")

    add_heading_2("7.2 Prim's Algorithm (Vertex-Centric)")
    add_bullet("Start with an initial landmark (e.g. 'Admin Block' as the Central Server / Network Operation Center).", "Step 1: ")
    add_bullet("Maintain a set of in-tree landmarks inMST and a Min-Heap of edges crossing the cut from inMST to unvisited landmarks.", "Step 2: ")
    add_bullet("Extract min-weight cut edge (u, v). Add v to inMST, add edge to tree, and push all incident edges from v into Min-Heap.", "Step 3: ")
    add_bullet("Repeat until all landmarks are included.", "Step 4: ")

    add_callout(
        "Kruskal vs. Prim Viva Question: When is Kruskal preferred over Prim? "
        "Answer: Kruskal is preferred on sparse graphs (E ≈ V) because sorting fewer edges is fast. "
        "Prim is preferred on dense graphs (E ≈ V^2) when implemented with an Adjacency Matrix or Fibonacci Heap (O(V^2) or O(E + V log V)).",
        "VIVA QUESTION: KRUSKAL VS PRIM COMPARISON"
    )

    # =========================================================================
    # SECTION 8: RESOURCE ALLOCATION (DYNAMIC PROGRAMMING)
    # =========================================================================
    add_heading_1("8. Campus Resource Allocation Optimizer (Dynamic Programming)")
    add_body(
        "A key requirement for college fests (e.g. Moksha, Taarangana) is venue scheduling: multiple student societies request prestigious venues "
        "(Main Auditorium, APJ Hall, Moksha Stage) with specific start times, end times, and expected attendance / utility scores. "
        "Two events cannot occupy the same venue simultaneously."
    )
    add_heading_2("Weighted Interval Scheduling Problem Formulation:")
    add_body("Each event i has start time s_i, finish time f_i, and utility value v_i.", bold_prefix="Inputs: ")
    add_body("Select a mutually compatible (non-overlapping) subset of events S such that sum(v_i for i in S) is maximized.", bold_prefix="Goal: ")
    add_body("Sort events by non-decreasing finish time: f_1 <= f_2 <= ... <= f_n.", bold_prefix="Step 1: ")
    add_body(
        "For each event i, find latest_non_conflict(i): the largest index j < i such that f_j <= s_i. "
        "This can be found via Binary Search in O(log n) time.",
        bold_prefix="Step 2: "
    )
    add_body(
        "Let DP[i] denote the maximum utility attainable considering events 1 through i:\n"
        "DP[i] = max( DP[i - 1],   v_i + DP[latest_non_conflict(i)] )\n"
        "• Case 1 (Exclude event i): The optimal utility is simply DP[i - 1].\n"
        "• Case 2 (Include event i): We gain utility v_i, plus the optimal utility from non-conflicting prior events DP[latest_non_conflict(i)].",
        bold_prefix="Bellman Recurrence Relation: "
    )
    add_body("Time: O(n log n) with binary search; Space: O(n).", bold_prefix="Complexity: ")
    add_bullet("Selected approved events (Debate, Taarangana Dance, Moksha Star Night) with 100% zero time conflicts and maximized 245 utility points.", "CampusNav Result: ")

    # =========================================================================
    # SECTION 9: SPECIALIZED FEATURES (INDOOR, ACCESSIBILITY, GEO)
    # =========================================================================
    add_heading_1("9. Advanced Real-World Engineering Features")
    
    add_heading_2("9.1 Indoor Corridor & Breezeway Walkway Modeling")
    add_body(
        "On the real NSUT campus, pedestrians frequently cut through buildings rather than walking around exterior perimeters. CampusNav models these real shortcuts:"
    )
    add_bullet("Direct indoor ground-floor traversal connecting North Academic lawns to South Administrative towers.", "Admin Block Indoor Breezeway: ")
    add_bullet("Central indoor lobby hallway connecting Department of Computer Engineering (COE) to Information Technology (IT).", "Block 6 Central Lobby: ")
    add_bullet("Pedestrian transit gate linking the central academic courtyard to the Training & Placement Cell.", "Gate between Block 5 & Central Library: ")

    add_heading_2("9.2 Accessibility Routing (Wheelchair & Reduced Mobility)")
    add_body(
        "All 1,564 edges carry an isAccessible boolean flag. Edges tagged as 'steps' or stairs are disqualified when the user activates the accessible toggle. "
        "The router automatically recalculates routes strictly along smooth paved paths, ramps, and elevator-accessible entrances."
    )

    add_heading_2("9.3 Dynamic Environmental Factors")
    add_bullet("Unpaved dirt paths ('track') receive a 1.5x weight penalty during rain simulation to guide users toward covered, paved walkways.", "Weather Multiplier: ")
    add_bullet("Corridors during class change intervals receive a 1.8x congestion multiplier, prompting Dijkstra to route through quieter alternate pathways.", "Rush-Hour Congestion: ")
    add_bullet("Users can simulate construction closures (e.g. Admin fountain repairs, Moksha stage construction) to observe live rerouting.", "Dynamic Road Closures: ")

    # =========================================================================
    # SECTION 10: TECH STACK JUSTIFICATION
    # =========================================================================
    add_heading_1("10. Technology Stack Selection & Architectural Rationale")
    
    tech_tbl = doc.add_table(rows=6, cols=3)
    tech_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_headers = ["Technology", "Role in Project", "Why Chosen (Technical Justification)"]
    t_data = [
        ["Vanilla JavaScript (ES6+)", "Client-side Controller & Algorithm Engine", "Zero framework overhead, direct DOM manipulation, instant mobile loading, zero bundle build steps."],
        ["Leaflet.js (v1.9.4)", "Lightweight Interactive Map Engine", "Only 42KB gzip footprint (vs Google Maps 250KB+). Native mobile touch support, smooth pinch-to-zoom, custom SVG renderers."],
        ["Carto Voyager & Esri Satellite", "Raster Tile Providers", "High-contrast street view for daytime navigation and high-resolution aerial satellite imagery for structural verification."],
        ["HTML5 Geolocation API", "Device Positioning", "Standardized browser API for continuous GPS watchPosition and real-time positioning on mobile."],
        ["CSS3 Modern Variables", "Responsive Design & Dark Theme", "Hardware-accelerated CSS transforms, responsive breakpoint system (mobile, tablet, desktop), seamless light/dark mode."]
    ]
    for c_i, h_text in enumerate(t_headers):
        c = tech_tbl.cell(0, c_i)
        set_cell_background(c, "1E3A8A")
        set_cell_margins(c, top=80, bottom=80, left=80, right=80)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_i, r_data in enumerate(t_data):
        for c_i, val in enumerate(r_data):
            c = tech_tbl.cell(r_i + 1, c_i)
            bg = "FFFFFF" if r_i % 2 == 0 else "F8FAFC"
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_i == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_PRIMARY

    p_spacer3 = doc.add_paragraph()
    p_spacer3.paragraph_format.space_after = Pt(8)

    # =========================================================================
    # SECTION 11: VIVA QUESTIONS & ANSWERS
    # =========================================================================
    add_heading_1("11. Anticipated Viva Voce Questions & Model Answers")

    viva_qa = [
        ("Q1: What is the exact graph representation used in CampusNav?",
         "CampusNav models the campus as a weighted, undirected graph G = (V, E) stored as an Adjacency List. |V| = 1,409 nodes representing surveyed path intersections and GPS points; |E| = 1,564 edges representing walkable walkways. The edge weights are calculated using the Haversine great-circle formula in meters."),

        ("Q2: Why does A* search evaluate significantly fewer nodes than Dijkstra?",
         "Dijkstra explores nodes blindly in all directions like an expanding concentric circle, because its priority is solely g(n) (cost from origin). A* uses f(n) = g(n) + h(n), where h(n) is the Haversine distance to the target. This prioritizes nodes that lie along the directional vector toward the goal, acting like a focused search beam rather than an expanding circle. On our graph, A* visits 122 nodes compared to Dijkstra's 610 nodes for the exact same path."),

        ("Q3: Can Dijkstra's algorithm work with negative edge weights? Does your project have negative weights?",
         "No, Dijkstra fails with negative edge weights because its greedy assumption—that once a node is popped from the priority queue its shortest distance is finalized—is violated. CampusNav only has non-negative edge weights (physical ground distances >= 0), so Dijkstra is guaranteed to be optimal."),

        ("Q4: Why did you implement a custom Binary Min-Heap instead of JavaScript's built-in Array.sort()?",
         "Calling Array.sort() on every iteration takes O(K log K) where K is the number of open nodes, degrading overall performance to O(V · K log K). A custom Min-Heap provides O(log V) insertion and extraction, keeping the algorithm within optimal O((V + E) log V) bounds."),

        ("Q5: What is heuristic admissibility and why is it essential?",
         "A heuristic h(n) is admissible if it never overestimates the true remaining cost to the goal (h(n) <= h*(n)). If a heuristic were to overestimate, A* might prematurely prune the true shortest path and return a suboptimal route. Because straight-line Haversine distance is the physical lower bound of distance between two points on a sphere, our heuristic is guaranteed to be admissible."),

        ("Q6: How does the Disjoint Set Union (DSU) structure prevent cycles in Kruskal's algorithm?",
         "DSU maintains disjoint sets of vertices. For each candidate edge (u, v), it executes find(u) and find(v). If find(u) == find(v), both vertices are already in the same connected tree, meaning adding (u, v) would create a cycle; hence it is rejected. If they differ, union(u, v) merges their sets and accepts the edge."),

        ("Q7: How did you implement indoor corridor navigation?",
         "We surveyed and placed internal walkthrough nodes along the central lobby of Block 6, the ground-floor breezeway of Admin Block, and the library breezeway gate. These nodes are linked via walkable edges with zero elevation penalty, allowing Dijkstra and A* to calculate paths through buildings when faster than walking around exterior perimeters."),

        ("Q8: How does the Dynamic Programming algorithm avoid event scheduling conflicts?",
         "It models the problem as Weighted Interval Scheduling. Events are sorted by finish times. For each event i, we compute the latest non-conflicting prior event j (f_j <= s_i). The Bellman recurrence DP[i] = max(DP[i-1], utility_i + DP[j]) evaluates whether including event i yields higher total utility than excluding it, guaranteeing non-overlapping schedules with optimal global utility in O(n log n) time."),

        ("Q9: What happens if a user's GPS signal is inaccurate or drifts?",
         "The HTML5 Geolocation API returns a coordinates object with an accuracy radius. CampusNav filters out points with excessive inaccuracy (> 50m) and tests whether the position is inside the campus boundary. If valid, it executes Spatial Snapping to project the point onto the nearest graph vertex and computes a smooth transition link."),

        ("Q10: Why choose Leaflet.js over Google Maps JavaScript API?",
         "Google Maps JavaScript API has a large bundle size (250KB+), requires external API keys with billing quotas, and renders map features on Google's closed proprietary servers. Leaflet.js is an open-source 42KB lightweight library that allows complete local control over custom SVG vector panes, custom divIcons, offline GeoJSON polygons, and zero external billing constraints."),

        ("Q11: How do you explain the project architecture to an examiner in under a minute?",
         "Explain the 4-tier client-side architecture: (1) Presentation Layer with Leaflet canvas and control UI; (2) Application Controller with state machine and GPS watcher; (3) Algorithmic Engine with Min-Heap, Dijkstra/A*, and DSU MST; (4) Topological Graph Data with 1,409 nodes and 1,564 edges. Explain that client-side execution delivers instantaneous sub-2ms routing with zero server latency."),

        ("Q12: How does the application scale if new buildings or blocks are constructed at NSUT?",
         "The graph topology in graphData.js is completely declarative. To add a new building, we append its junction nodes to the node list and connect them via bidirectional edge definitions with distance and accessibility tags. No algorithmic or controller code needs modification.")
    ]

    for q, a in viva_qa:
        add_body(q, bold_prefix="• ", space_after=2)
        p_ans = add_body(a, bold_prefix="Answer: ", space_after=6)
        p_ans.paragraph_format.left_indent = Inches(0.2)

    # Save Document
    doc.save(output_path)
    print(f"Document saved successfully as: {output_path}")

if __name__ == "__main__":
    create_viva_document("CampusNav_Viva_Comprehensive_Notes.docx")
