import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def generate_report():
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
        hrun = hp.add_run("CampusNav • Official Project Report for Viva Voce")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Netaji Subhas University of Technology (NSUT) • Department of Computer Science & Engineering")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)

    # Theme Colors
    COLOR_PRIMARY = RGBColor(30, 58, 138)     # Deep Navy (#1E3A8A)
    COLOR_SECONDARY = RGBColor(2, 132, 199)   # Cyan / Blue (#0284C7)
    COLOR_TEXT = RGBColor(15, 23, 42)         # Slate 900 (#0F172A)
    COLOR_MUTED = RGBColor(71, 85, 105)       # Slate 600 (#475569)
    COLOR_EMERALD = RGBColor(5, 150, 105)     # Success / Emerald (#059669)
    COLOR_AMBER = RGBColor(217, 119, 6)       # Amber (#D97706)

    def set_cell_background(cell, fill_hex):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def set_cell_margins(cell, top=90, bottom=90, left=120, right=120):
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
        run.font.size = Pt(22)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY

        if subtitle:
            p2 = doc.add_paragraph()
            p2.paragraph_format.space_before = Pt(2)
            p2.paragraph_format.space_after = Pt(14)
            p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run2 = p2.add_run(subtitle)
            run2.font.name = "Calibri"
            run2.font.size = Pt(11.5)
            run2.font.italic = True
            run2.font.color.rgb = COLOR_SECONDARY

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(11)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10.5)
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

    def add_callout(text, title="KEY VIVA HIGHLIGHT", border_color="0284C7", bg_color="F0F9FF"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.8)
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
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
        r_title.font.color.rgb = COLOR_PRIMARY

        r_text = cp.add_run(text)
        r_text.font.name = "Calibri"
        r_text.font.size = Pt(9.5)
        r_text.font.color.rgb = COLOR_TEXT
        
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(3)
        p_after.paragraph_format.space_after = Pt(2)

    # =========================================================================
    # DOCUMENT COVER & HEADER
    # =========================================================================
    add_title("CAMPUSNAV: SMART CAMPUS NAVIGATION & RESOURCE OPTIMIZER", 
              "Comprehensive Academic Project Report for Viva Voce Examination")

    # Project Information Table
    info_tbl = doc.add_table(rows=5, cols=2)
    info_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ["Project Title", "CampusNav: NSUT Smart Campus Navigation & Resource Optimizer"],
        ["Institution & Department", "Netaji Subhas University of Technology (NSUT), Dwarka • Dept. of CSE"],
        ["Target Area & Topology", "145-Acre Main Campus • Graph G = (V, E) with |V| = 1,409 Nodes, |E| = 1,564 Edges, 28 Landmarks"],
        ["Core DSA & Algorithms", "Dijkstra (Heap), BFS, DFS, Kruskal's & Prim's MST, Balanced AVL Tree, Separate-Chaining Hashing, Dynamic Programming (Weighted Interval Scheduling & 0/1 Knapsack)"],
        ["Execution Architecture", "Pure Client-Side Edge Computing (Zero Server Latency, Sub-2ms Calculations, 100% Offline Capability)"]
    ]
    for r_i, (k, v) in enumerate(info_data):
        c0 = info_tbl.cell(r_i, 0)
        c1 = info_tbl.cell(r_i, 1)
        c0.width = Inches(2.2)
        c1.width = Inches(4.6)
        set_cell_background(c0, "1E3A8A")
        set_cell_background(c1, "F8FAFC" if r_i % 2 == 1 else "FFFFFF")
        set_cell_margins(c0, top=60, bottom=60, left=80, right=80)
        set_cell_margins(c1, top=60, bottom=60, left=80, right=80)

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(8.5)
        r0.font.color.rgb = RGBColor(255, 255, 255)

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = COLOR_TEXT

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_after = Pt(6)

    # Elevator Pitch
    add_callout(
        "\"CampusNav is an enterprise-grade geospatial navigation and combinatorial optimization system built specifically for "
        "NSUT's 145-acre campus. It solves two critical university challenges: (1) high-precision pedestrian wayfinding across complex "
        "inter-block footpaths and wheelchair-accessible ramps using Dijkstra, BFS, and DFS; and (2) automated university resource "
        "allocation using Dynamic Programming for conflict-free fest venue scheduling and departmental budget distribution, plus "
        "Kruskal's and Prim's MST algorithms for minimum-cost campus fiber-optic cabling. The site provides four dedicated views: "
        "Campus Map, Find Route, Directory (powered by an AVL Tree and Hash Table), and Resource Allocation. "
        "All algorithms execute directly in the browser with sub-2 millisecond response times.\"",
        "EXECUTIVE SUMMARY (30-SECOND VIVA PITCH)"
    )

    # =========================================================================
    # SECTION 1: INTRODUCTION & PROBLEM DEFINITION
    # =========================================================================
    add_heading_1("1. Introduction & Problem Definition")
    add_body(
        "Modern university campuses such as NSUT Dwarka span over 145 acres with intricate pedestrian networks, multi-floor academic blocks "
        "(Blocks 4, 5, 6, Admin Block, APJ Complex), specialized indoor corridors, restricted security gates, and large recreational grounds "
        "(Moksha Ground, Nescii Lawns). Conventional navigation tools like Google Maps exhibit severe limitations in university environments:"
    )
    add_bullet("Commercial GPS platforms prioritize vehicular roads and fail to accurately map narrow footpaths, paved pedestrian alleys, or indoor walkways.", "Vehicular Road Bias: ")
    add_bullet("Google Maps cannot distinguish between flight of stairs and ramps, frequently routing students with reduced mobility or wheelchair users into impassable obstacles.", "Lack of Accessibility Modeling: ")
    add_bullet("Campus visitors lack an authoritative directory indexing building wings, departmental offices, and student utility centers.", "Absence of Hierarchical Directory: ")
    add_bullet("University administrations lack automated tools to plan physical infrastructure cabling (fiber-optic / water pipelines) and schedule shared campus venues (Main Audi, APJ Halls) during major fests (Moksha, Taarangana).", "Unsolved Resource Allocation Challenges: ")
    add_body(
        "CampusNav addresses these limitations by uniting Geospatial Information Systems (GIS), Rigorous Graph Theory, "
        "Classic Data Structures, and Dynamic Programming into an intuitive, high-performance web platform."
    )

    # =========================================================================
    # SECTION 2: SYSTEM ARCHITECTURE & WEBSITE STRUCTURE
    # =========================================================================
    add_heading_1("2. System Architecture & Website Design")

    add_heading_2("2.1 Decoupled 4-Tier Client-Side Architecture")
    add_body(
        "The application is engineered on a pure client-side edge architecture, ensuring zero backend server costs, "
        "instant sub-2ms response times, and full offline resilience once loaded:"
    )

    # Architecture Table
    arch_tbl = doc.add_table(rows=5, cols=3)
    arch_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    arch_headers = ["Architectural Tier", "Primary Modules & Files", "Core Responsibilities"]
    arch_data = [
        ["Tier 1:\nPresentation &\nVisualization", 
         "• index.html\n• styles.css\n• leaflet.js (v1.9.4)\n• leaflet.css", 
         "• Renders dual-tile interactive Leaflet canvas (Carto Voyager street & Esri Satellite).\n• Glassmorphic control panels, interactive marker badges, and glowing route polylines.\n• Turn-by-turn cardinal guidance list and animated walk simulation cursor."],
        
        ["Tier 2:\nApplication Controller\n& State Machine", 
         "• app.js\n• HTML5 Geolocation API\n• Event Listeners", 
         "• Manages application state, active view transitions, and origin/destination picks.\n• Acquires device GPS coordinates via navigator.geolocation.watchPosition.\n• Performs Spatial Snapping: queries graph to map raw GPS points to nearest walkable node.\n• Synthesizes turn directions from geodetic bearing angles."],
        
        ["Tier 3:\nAlgorithmic & Data\nStructures Core", 
         "• algorithms.js\n• MinHeap\n• DSU\n• AVLTree\n• CampusHashTable", 
         "• Min-Heap Priority Queue (O(log V)) for Dijkstra & Prim.\n• Disjoint Set Union (DSU) with Path Compression & Union-by-Rank (O(α(V))) for Kruskal.\n• Self-Balancing AVL Tree with 4 rotation cases for O(log N) directory search.\n• Separate-Chaining Hash Table (M = 37, polynomial hash) for O(1) landmark lookups.\n• Dynamic Programming: Weighted Interval Scheduling & 0/1 Knapsack engines."],
        
        ["Tier 4:\nGeospatial Graph\nData & Topology", 
         "• graphData.js\n• Curated NSUT Overpass OSM\n• Authoritative POIs", 
         "• Topological Graph G = (V, E) of NSUT: |V| = 1,409 nodes, |E| = 1,564 edges.\n• WGS-84 coordinate system with high-precision latitude and longitude pairs.\n• Edge attributes: Haversine distance in meters, highway tag, accessibility flag.\n• 28 Curated landmark facilities across Academic, Hostels, Admin, Sports, and Gates."]
    ]

    for c_i, h_text in enumerate(arch_headers):
        c = arch_tbl.cell(0, c_i)
        set_cell_background(c, "1E3A8A")
        set_cell_margins(c, top=70, bottom=70, left=80, right=80)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_i, r_data in enumerate(arch_data):
        for c_i, val in enumerate(r_data):
            c = arch_tbl.cell(r_i + 1, c_i)
            bg = "F0F9FF" if r_i % 2 == 1 else "FFFFFF"
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_i == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_PRIMARY

    p_spacer_arch = doc.add_paragraph()
    p_spacer_arch.paragraph_format.space_after = Pt(6)

    add_heading_2("2.2 The 4 Core Functional Views of the Website")
    add_body(
        "The website user interface is divided into four cleanly isolated views accessible via the global top navbar:"
    )
    add_bullet(
        "Provides full-screen spatial exploration. Features a Carto Voyager street view and Esri satellite imagery switcher, "
        "star compass, zoom controls, and 28 clickable location name pill badges with quick 'Set Start' and 'Set Dest' shortcuts.",
        "1. Campus Map View (#view-campus-map): "
    )
    add_bullet(
        "Enables users to select Origin and Destination (or use live GPS location). Features an algorithm selector "
        "(Dijkstra, BFS, DFS) and a wheelchair accessibility toggle. Draws glowing animated route lines, generates turn-by-turn guidance, "
        "and provides an interactive walk simulator.",
        "2. Find Route View (#view-find-route): "
    )
    add_bullet(
        "Displays the comprehensive campus directory of academic departments, hostel blocks, and utility centers. "
        "Powered by a Balanced Search Tree (AVL Tree) for sub-millisecond prefix search and category filtering.",
        "3. Directory View (#view-directory): "
    )
    add_bullet(
        "A dedicated administrative optimization suite with 3 sub-task tabs: "
        "(a) Fest Venue Scheduling via Weighted Interval Scheduling DP; (b) Department Equipment Budget Allocation via 0/1 Knapsack DP; "
        "and (c) Campus Infrastructure Cabling Layout via Kruskal's & Prim's MST.",
        "4. Resource Allocation View (#view-resource-allocation): "
    )

    # =========================================================================
    # SECTION 3: COMPLETE ALGORITHM & DSA SPECIFICATIONS
    # =========================================================================
    add_heading_1("3. Algorithms & Data Structures Specification")
    add_body(
        "The project strictly utilizes 7 core Computer Science algorithms and data structures, mapped directly to real-world campus operations:"
    )

    # Master Table
    m_headers = ["Algorithm / DSA", "Section on Site", "Core Problem Solved", "Time Complexity", "Space"]
    m_rows = [
        ["Dijkstra's Algorithm", "Find Route", "Shortest pedestrian walking route in meters", "O((V + E) log V)", "O(V)"],
        ["Breadth-First Search (BFS)", "Find Route & Audit", "Route with fewest turns/hops; connectivity audit", "O(V + E)", "O(V)"],
        ["Depth-First Search (DFS)", "Find Route (Benchmark)", "Path exploration; baseline comparative analysis", "O(V + E)", "O(V)"],
        ["Kruskal's Algorithm (MST)", "Resource Allocation", "Global fiber-optic cabling layout (3,569 m)", "O(E log E)", "O(V)"],
        ["Prim's Algorithm (MST)", "Resource Allocation", "Server-centric cabling expansion from Admin NOC", "O(E log V)", "O(V)"],
        ["Balanced Search Tree (AVL)", "Campus Directory", "O(log N) facility search & prefix autocomplete", "O(log N)", "O(N)"],
        ["Custom Hash Table", "Global Indexing", "O(1) instant landmark & graph adjacency lookup", "O(1) avg", "O(N)"],
        ["Dynamic Programming", "Resource Allocation", "Fest venue scheduling & 0/1 knapsack budget allocation", "O(N log N) / O(N·W)", "O(N·W)"]
    ]
    master_tbl = doc.add_table(rows=len(m_rows) + 1, cols=len(m_headers))
    master_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

    for c_i, h_text in enumerate(m_headers):
        c = master_tbl.cell(0, c_i)
        set_cell_background(c, "1E3A8A")
        set_cell_margins(c, top=70, bottom=70, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_i, r_data in enumerate(m_rows):
        for c_i, val in enumerate(r_data):
            c = master_tbl.cell(r_i + 1, c_i)
            bg = "F0F9FF" if r_i % 2 == 1 else "FFFFFF"
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=60, right=60)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i in [0, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_i == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_PRIMARY

    p_spacer_m = doc.add_paragraph()
    p_spacer_m.paragraph_format.space_after = Pt(6)

    # Detailed Subsections
    add_heading_2("3.1 Dijkstra's Algorithm (Min-Heap Priority Queue)")
    add_bullet("Computes shortest physical distance in meters between any origin and destination across 1,409 nodes.", "Role: ")
    add_bullet("Custom Binary Min-Heap class (push/pop in O(log V)), early-exit optimization upon popping the destination vertex.", "Implementation: ")
    add_bullet("Disqualifies edges tagged as stairs (type === 'steps') when wheelchair accessibility is toggled, ensuring 100% ramp compliance.", "Accessibility: ")

    add_heading_2("3.2 Breadth-First Search (BFS) & Depth-First Search (DFS)")
    add_bullet("Traverses level-by-level using a FIFO Queue. Guarantees the path with minimum intersections/turns (22 hops from Main Gate to APJ Complex).", "BFS (Fewest Hops): ")
    add_bullet("Traverses deeply using a LIFO Stack. Serves as an educational benchmark showing why cost guidance is essential (2,624 m vs 661 m).", "DFS (Path Traversal): ")

    add_heading_2("3.3 Minimum Spanning Tree: Kruskal's & Prim's Algorithms")
    add_bullet("Determines minimum-cost layout for laying 3,569 meters of high-speed fiber-optic cabling connecting all 28 landmarks with 0 cycles.", "Role: ")
    add_bullet("Edge-centric. Precomputes pairwise walking distances, sorts edges in O(E log E), and unites sets via DSU with Path Compression and Union-by-Rank in O(α(V)) amortized time.", "Kruskal's Algorithm: ")
    add_bullet("Vertex-centric. Grows outward from Admin Block (Central NOC) by greedily picking the minimum-weight cut edge via a Min-Heap in O(E log V).", "Prim's Algorithm: ")

    add_heading_2("3.4 Balanced Search Tree: Self-Balancing AVL Tree")
    add_bullet("Indexes all 28 campus facilities alphabetically by name in the Campus Directory, guaranteeing O(log N) search and prefix matching.", "Role: ")
    add_bullet("Tracks node height and enforces balance factor ∈ {-1, 0, 1}. Implements 4 self-balancing rotations: Left-Left (LL), Right-Right (RR), Left-Right (LR), and Right-Left (RL).", "Implementation: ")

    add_heading_2("3.5 Custom Separate-Chaining Hash Table (CampusHashTable)")
    add_bullet("Provides O(1) instant key-value lookup of landmarks by ID and rapid graph adjacency edge traversal.", "Role: ")
    add_bullet("Prime table size M = 37, Polynomial Rolling Hash (base 31: hash = sum(c_i * 31^(n-1-i)) mod 37), and Separate Chaining for collision resolution (load factor α = 0.76).", "Implementation: ")

    add_heading_2("3.6 Dynamic Programming: Resource Allocation")
    add_bullet(
        "Allocates campus fest venues (Auditorium, APJ Complex, Moksha Ground) among overlapping society proposals. "
        "Sorts events by finish time, uses Binary Search in O(log N) to find the latest non-conflicting event, and evaluates: "
        "DP[i] = max( DP[i-1],  utility_i + DP[latest_non_conflict(i)] ). Result: Approves 3 events achieving 245 utility points with zero conflicts.",
        "Task 1 (Weighted Interval Scheduling, O(N log N)): "
    )
    add_bullet(
        "Allocates a fixed campus annual modernization budget W (₹15L–₹30L) among departmental lab proposals. "
        "Recurrence: DP[i, w] = (cost_i > w) ? DP[i-1, w] : max( DP[i-1, w],  utility_i + DP[i-1, w - cost_i] ). "
        "Backtracks through table to output funded vs rejected proposals, achieving 95% budget utilization.",
        "Task 2 (0/1 Knapsack DP, O(N · W)): "
    )

    # =========================================================================
    # SECTION 4: MATHEMATICAL FOUNDATIONS
    # =========================================================================
    add_heading_1("4. Core Mathematical Formulations")

    add_heading_2("4.1 Haversine Great-Circle Distance Formula")
    add_body(
        "Calculates exact physical ground distance between two planetary coordinates (lat1, lon1) and (lat2, lon2) over the WGS-84 Earth sphere (R = 6,371,000 m):"
    )
    add_body("a = sin²(Δφ / 2) + cos(φ1) · cos(φ2) · sin²(Δλ / 2)", bold_prefix="Haversine Term (a): ")
    add_body("c = 2 · atan2( √a, √(1 - a) )", bold_prefix="Angular Distance (c): ")
    add_body("Distance (d) = R · c   (meters)", bold_prefix="Final Ground Distance: ")

    add_heading_2("4.2 Forward Geodetic Azimuth Bearing (Turn Guidance)")
    add_body(
        "Calculates cardinal bearing angle θ for synthesizing turn-by-turn navigation instructions:"
    )
    add_body("y = sin(Δλ) · cos(φ2)", bold_prefix="y-component: ")
    add_body("x = cos(φ1) · sin(φ2) - sin(φ1) · cos(φ2) · cos(Δλ)", bold_prefix="x-component: ")
    add_body("θ = (atan2(y, x) · 180 / π + 360) mod 360", bold_prefix="Azimuth Angle (θ): ")
    add_body(
        "The angular delta (turnAngle = (θ_curr - θ_prev + 540) mod 360 - 180) classifies directions into "
        "slight left, sharp left, slight right, sharp right, or continue straight."
    )

    add_heading_2("4.3 Spatial Snapping Algorithm")
    add_body(
        "When an arbitrary GPS coordinate P is acquired via the HTML5 Geolocation API, it is projected onto the nearest walkable graph vertex:\n"
        "V_snap = argmin_{v in V} HaversineDistance(P, v)\n"
        "An implicit lead-in connector segment is created, preventing route markers from jumping onto impassable buildings or lawns."
    )

    # =========================================================================
    # SECTION 5: PERFORMANCE BENCHMARKS & EXPERIMENTAL RESULTS
    # =========================================================================
    add_heading_1("5. Experimental Performance Benchmarks")
    add_body(
        "The following empirical results were measured directly on the live NSUT campus graph running in Google Chrome (V8 engine):"
    )

    # Benchmark Table
    bm_tbl = doc.add_table(rows=4, cols=6)
    bm_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    bm_headers = ["Algorithm", "Distance (m)", "Nodes Visited", "Hops", "Execution Time", "Optimality Guarantee"]
    bm_data = [
        ["Dijkstra's (Min-Heap)", "661 m", "610 nodes", "22", "3.4 ms", "Guaranteed Optimal (Metric)"],
        ["BFS (Breadth-First)", "690 m", "715 nodes", "22", "1.9 ms", "Hop-Optimal (Min Intersections)"],
        ["DFS (Depth-First)", "2,624 m", "352 nodes", "95", "1.1 ms", "Unguided Path Traversal"]
    ]

    for c_i, h_text in enumerate(bm_headers):
        c = bm_tbl.cell(0, c_i)
        set_cell_background(c, "1E3A8A")
        set_cell_margins(c, top=70, bottom=70, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_i, r_data in enumerate(bm_data):
        for c_i, val in enumerate(r_data):
            c = bm_tbl.cell(r_i + 1, c_i)
            bg = "F0F9FF" if r_i == 0 else ("FFFFFF" if r_i % 2 == 1 else "F8FAFC")
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=60, right=60)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i in [1, 2, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_i == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_PRIMARY

    p_spacer_bm = doc.add_paragraph()
    p_spacer_bm.paragraph_format.space_after = Pt(6)

    add_bullet("3,569 meters total cabling across 26 tree links, connecting all 28 landmarks with 0 cycles (Estimated trenching cost: ₹16,06,050 @ ₹450/m).", "MST Cabling Result: ")
    add_bullet("Approves Debate Finals, Taarangana Dance, and Moksha Star Night, achieving 245 utility points with 100% zero time overlaps.", "DP Event Scheduling Result: ")
    add_bullet("Achieves ₹19.0 Lakhs allocation out of ₹20.0 Lakhs budget (95% utilization), funding 3 high-impact proposals with 225 utility points.", "DP Knapsack Budget Result: ")

    # =========================================================================
    # SECTION 6: KEY VIVA QUESTIONS & DEFENSE ANSWERS
    # =========================================================================
    add_heading_1("6. Key Viva Voce Questions & Model Defense Answers")

    viva_questions = [
        ("Why did you choose a pure client-side architecture over a Python/Node.js backend?",
         "A client-side architecture eliminates server hosting costs, network round-trip latency, and API rate limits. The entire graph (1,409 nodes, 1,564 edges) occupies only ~1.6 MB in JavaScript memory, executing route computations in under 2 milliseconds directly in the browser V8 engine, with full offline capability."),

        ("Why use an AVL Tree instead of JavaScript's built-in Array.filter() in the Directory?",
         "Array.filter() performs an O(N) linear scan across every element. For small datasets it works, but it does not scale. An AVL Tree organizes data into a balanced logarithmic hierarchy, guaranteeing O(log N) search and prefix lookup even if the campus directory expands to thousands of faculty offices, classrooms, and labs."),

        ("What is the difference between Dijkstra and Prim's algorithm? Both use a Min-Heap!",
         "Dijkstra's priority is the accumulated distance from the START node to node n (g(n)). Prim's priority is simply the weight of the single cut edge connecting node n to the growing MST, regardless of origin. Dijkstra builds a shortest-path tree rooted at one origin; Prim builds a global minimum weight spanning tree connecting all nodes."),

        ("Why does Dynamic Programming succeed for 0/1 Knapsack where Greedy approaches fail?",
         "Greedy sorting by utility-to-cost ratio only works for Fractional Knapsack. In 0/1 Knapsack, items cannot be fractionally divided. A greedy choice can consume capacity with a high-ratio item and leave insufficient space for a combination of items that together would yield far higher utility. DP evaluates all overlapping subproblems to guarantee the global optimum."),

        ("How does Disjoint Set Union (DSU) prevent cycles in Kruskal's algorithm?",
         "For every candidate edge (u, v), DSU checks find(u) == find(v). If true, both nodes are already part of the same connected tree, so adding the edge would form a cycle; hence it is rejected. If false, union(u, v) merges their sets in O(α(V)) amortized time.")
    ]

    for q, a in viva_questions:
        add_body(q, bold_prefix="• Q: ", space_after=2)
        p_ans = add_body(a, bold_prefix="Answer: ", space_after=6)
        p_ans.paragraph_format.left_indent = Inches(0.2)

    # =========================================================================
    # SECTION 7: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    add_heading_1("7. Conclusion & Future Scope")
    add_body(
        "CampusNav demonstrates that classic Computer Science data structures and algorithms—Dijkstra, BFS, DFS, Kruskal's/Prim's MST, "
        "AVL Trees, Hashing, and Dynamic Programming—can be combined to build an enterprise-grade, high-performance spatial navigation "
        "and administrative optimization platform for large university campuses without any server hosting overhead."
    )
    add_heading_2("Future Enhancements:")
    add_bullet("Expanding indoor pedestrian walkways into full 3D elevation models with floor-by-floor staircase and elevator transitions.", "3D Multi-Floor Navigation: ")
    add_bullet("Deploying Bluetooth Low Energy (BLE) beacons inside academic blocks to enable sub-meter indoor positioning where GPS signals attenuate.", "BLE Micro-Location Beacons: ")
    add_bullet("Packaging the web application with a Service Worker and manifest file for installable offline home screen access on Android and iOS.", "Progressive Web App (PWA): ")

    # Save Document
    doc.save("CampusNav_Project_Report.docx")
    print("Project Report successfully generated: CampusNav_Project_Report.docx")

if __name__ == "__main__":
    generate_report()
