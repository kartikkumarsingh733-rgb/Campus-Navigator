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
        set_cell_background(cell, "F0F9FF")
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
              "Core Algorithms & Data Structures Examination Guide")

    # Metadata Box
    meta_tbl = doc.add_table(rows=2, cols=3)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_headers = ["Institution", "Domain", "Required Algorithms & Data Structures"]
    meta_values = [
        "Netaji Subhas University of Technology (NSUT)", 
        "Graph Theory, Geospatial Systems & Optimization", 
        "BFS, DFS, Dijkstra, Kruskal/Prim MST, Balanced Search Tree (AVL), Hashing, Dynamic Programming"
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
    # SECTION 1: SYSTEM OVERVIEW & 4 APPLICATION SECTIONS
    # =========================================================================
    add_heading_1("1. Project Architecture & Four Core Application Sections")
    add_body(
        "CampusNav is organized into four clean, specialized functional sections designed to address both individual student "
        "pedestrian navigation and university-wide operational resource allocation across NSUT's 145-acre campus:"
    )

    sec_tbl = doc.add_table(rows=5, cols=3)
    sec_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    sec_headers = ["Section", "Core Purpose", "Underlying Algorithms & Data Structures"]
    sec_data = [
        ["1. Campus Map", "Interactive dual-layer GIS visualization (Street + Satellite) with 28 facility markers.", "OpenStreetMap GeoJSON, Spatial Snapping, Coordinate Hashing."],
        ["2. Find Route", "Turn-by-turn shortest and fewest-turn pedestrian routing with wheelchair accessibility.", "Dijkstra's Algorithm (Min-Heap), Breadth-First Search (BFS), Depth-First Search (DFS)."],
        ["3. Directory", "Search, filter, and inspect campus academic, administrative, hostel, and sports facilities.", "Balanced Search Tree (AVL Tree with O(log N) prefix search) & Custom Separate-Chaining Hash Table."],
        ["4. Resource Allocation", "Optimizes fest venue schedules, department equipment budgets, and infrastructure utility layout.", "Dynamic Programming (Weighted Interval Scheduling & 0/1 Knapsack) + Minimum Spanning Trees (Kruskal & Prim)."]
    ]

    for c_i, h_text in enumerate(sec_headers):
        c = sec_tbl.cell(0, c_i)
        set_cell_background(c, "1E3A8A")
        set_cell_margins(c, top=80, bottom=80, left=90, right=90)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_i, r_data in enumerate(sec_data):
        for c_i, val in enumerate(r_data):
            c = sec_tbl.cell(r_i + 1, c_i)
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

    p_spacer_sec = doc.add_paragraph()
    p_spacer_sec.paragraph_format.space_after = Pt(8)

    add_callout(
        "\"CampusNav operates on a Decoupled Client-Side Architecture powered strictly by 7 classic Computer Science paradigms: "
        "Dijkstra, BFS, DFS, Kruskal's/Prim's MST, Balanced Search Trees (AVL), Hashing, and Dynamic Programming. "
        "The application provides four primary sections: Campus Map for spatial discovery, Find Route for ground routing, "
        "Directory powered by an AVL Tree for logarithmic facility lookup, and a dedicated Resource Allocation section solving "
        "festival venue scheduling and departmental budget optimization via Dynamic Programming, as well as fiber cabling via MST. "
        "All algorithms execute directly in the browser with sub-2ms response times.\"",
        "30-SECOND ELEVATOR PITCH FOR YOUR PROFESSOR"
    )

    # =========================================================================
    # SECTION 2: ALGORITHM & DATA STRUCTURE MAPPING
    # =========================================================================
    add_heading_1("2. Exact Algorithm-to-Task Mapping")
    add_body("Every algorithm and data structure in the codebase maps to an explicit, real-world task on the NSUT campus:")

    algo_matrix = [
        ("1. Dijkstra's Algorithm", "Find Route Section", "Calculates the mathematically guaranteed shortest walking path in meters using a Binary Min-Heap Priority Queue (Time: O((V + E) log V))."),
        ("2. Breadth-First Search (BFS)", "Find Route & Connectivity", "Finds the path with the minimum number of intersections/turns (fewest hops), and validates strong connectivity across all 1,409 nodes."),
        ("3. Depth-First Search (DFS)", "Find Route (Benchmark)", "Performs deep unguided branch traversal to demonstrate path exploration and provide a baseline comparison showing why cost-guided search is essential."),
        ("4. Kruskal's Algorithm (MST)", "Resource Allocation Section", "Computes the global Minimum Spanning Tree across all 28 landmarks for fiber-optic internet cabling (3,569 m total) using Disjoint Set Union (DSU)."),
        ("5. Prim's Algorithm (MST)", "Resource Allocation Section", "Computes the Minimum Spanning Tree vertex-by-vertex starting outward from the Central Server / NOC (Admin Block) using a Min-Heap."),
        ("6. Balanced Search Tree (AVL Tree)", "Campus Directory Section", "Indexes all 28 campus facilities alphabetically by name with guaranteed O(log N) search, logarithmic prefix autocomplete, and in-order traversal."),
        ("7. Custom Hash Table (Hashing)", "Graph & Directory Indexing", "Provides O(1) instant key-value lookup of landmarks by ID/name and adjacency list edges using a Polynomial Rolling Hash with Separate Chaining."),
        ("8. DP: Weighted Interval Scheduling", "Resource Allocation Section", "Allocates high-demand campus fest venues (Auditorium, APJ Complex, Moksha Ground) among overlapping society proposals to maximize utility without conflicts (O(N log N))."),
        ("9. DP: 0/1 Knapsack Problem", "Resource Allocation Section", "Allocates a fixed campus annual modernization budget among departmental lab and equipment proposals to maximize academic utility (O(N · W)).")
    ]

    for title, where, desc in algo_matrix:
        add_body(f"• {title} [{where}]: ", bold_prefix="", space_after=1)
        p_desc = add_body(desc, space_after=4)
        p_desc.paragraph_format.left_indent = Inches(0.2)

    # =========================================================================
    # SECTION 3: BALANCED SEARCH TREE (AVL TREE) & HASHING
    # =========================================================================
    add_heading_1("3. Balanced Search Tree (AVL Tree) & Custom Hashing")

    add_heading_2("3.1 Balanced Search Tree: AVL Tree Implementation")
    add_body(
        "A standard Binary Search Tree (BST) can degrade to O(N) linear time if keys are inserted in sorted order (skewed tree). "
        "CampusNav implements a self-balancing AVL Tree where for every node, the height difference between left and right subtrees "
        "(Balance Factor = height(left) - height(right)) is strictly in {-1, 0, 1}."
    )
    add_bullet("Left-Left (LL) Imbalance (Balance > 1, key < node.left.key): Resolved by a single Right Rotation (rotateRight).", "LL Case: ")
    add_bullet("Right-Right (RR) Imbalance (Balance < -1, key > node.right.key): Resolved by a single Left Rotation (rotateLeft).", "RR Case: ")
    add_bullet("Left-Right (LR) Imbalance: Resolved by a Left Rotation on node.left, followed by a Right Rotation on node.", "LR Case: ")
    add_bullet("Right-Left (RL) Imbalance: Resolved by a Right Rotation on node.right, followed by a Left Rotation on node.", "RL Case: ")
    add_bullet(
        "All 28 campus facilities are inserted into the AVL tree. The search bar in the Directory executes searchPrefix(query) "
        "in guaranteed O(log N) time. The tree maintains a height of 6 for 28 nodes (log2(28) ≈ 4.8), ensuring optimal balance.",
        "Application in Campus Directory: "
    )

    add_heading_2("3.2 Custom Hash Table (Hashing)")
    add_body(
        "CampusNav implements a custom Separate-Chaining Hash Table (CampusHashTable) with table size M = 37 (a prime number to minimize collisions). "
        "The hash code is calculated using a Polynomial Rolling Hash:"
    )
    add_body("hash(str) = ( sum_{i=0}^{len-1} (str.charCodeAt(i) · 31^{len-1-i}) ) mod M", bold_prefix="Polynomial Hash Formula: ")
    add_body(
        "Collisions are resolved via Separate Chaining (bucket arrays). With 28 items in a 37-bucket table, the load factor is α = 28/37 ≈ 0.76. "
        "This guarantees O(1) average-case time complexity for landmark lookup by ID (e.g. hashTable.get('main_gate')).",
        bold_prefix="Collision Resolution & Load Factor: "
    )

    # =========================================================================
    # SECTION 4: ROUTING ALGORITHMS (DIJKSTRA, BFS, DFS)
    # =========================================================================
    add_heading_1("4. Ground Routing Algorithms (Dijkstra, BFS, DFS)")

    add_heading_2("4.1 Dijkstra's Algorithm (Min-Heap)")
    add_body(
        "Dijkstra's algorithm computes the shortest path between origin and destination on the weighted graph G = (V, E) (|V|=1,409, |E|=1,564). "
        "A custom in-memory Binary Min-Heap Priority Queue ensures O(log V) push and pop operations, achieving O((V + E) log V) total runtime."
    )
    add_bullet("As soon as the destination vertex u == endNode is popped from the min-heap, the loop terminates immediately.", "Early-Exit Optimization: ")
    add_bullet("When wheelchair accessibility is enabled, edges tagged with type === 'steps' are bypassed, routing exclusively along ramps.", "Accessibility Filter: ")

    add_heading_2("4.2 Breadth-First Search (BFS) vs. Depth-First Search (DFS)")
    add_bullet("Traverses radially level-by-level using a FIFO Queue. Guarantees the fewest intersection turns/hops (e.g. 22 hops).", "BFS (Unweighted Hops): ")
    add_bullet("Traverses deeply using a LIFO Stack without cost guidance. Demonstrates how unguided exploration yields extreme path lengths (2,624 m vs 661 m).", "DFS (Path Traversal): ")

    # Table: Algorithm Comparison
    add_heading_3("Algorithm Benchmark Comparison on NSUT Graph (Main Gate → APJ Complex):")
    algo_tbl = doc.add_table(rows=4, cols=5)
    algo_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Algorithm", "Distance (m)", "Nodes Visited", "Time (ms)", "Optimality Guarantee"]
    rows_data = [
        ["Dijkstra's (Min-Heap)", "661 m", "610 nodes", "3.4 ms", "Guaranteed Optimal (Metric)"],
        ["BFS (Breadth-First)", "690 m", "715 nodes", "1.9 ms", "Hop-Optimal (Min Turns: 22)"],
        ["DFS (Depth-First)", "2,624 m", "352 nodes", "1.1 ms", "Unguided Path Traversal"]
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
            bg = "F0F9FF" if r_i == 0 else ("FFFFFF" if r_i % 2 == 1 else "F8FAFC")
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i in [1, 2, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if r_i == 0 and c_i == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_PRIMARY

    p_spacer2 = doc.add_paragraph()
    p_spacer2.paragraph_format.space_after = Pt(8)

    # =========================================================================
    # SECTION 5: RESOURCE ALLOCATION VIA DYNAMIC PROGRAMMING
    # =========================================================================
    add_heading_1("5. Dynamic Programming for Campus Resource Allocation")

    add_heading_2("5.1 Task 1: Fest Venue & Event Allocation (Weighted Interval Scheduling)")
    add_body(
        "Student societies (Moksha Council, Taarangana, CSI, IEEE, Debating Society) request campus venues (Main Auditorium, APJ Complex, SAC, Moksha Ground) "
        "with specific start times s_i, end times f_i, and utility/attendance values v_i. Two events cannot overlap in the same venue."
    )
    add_body("Events are sorted by non-decreasing finish times f_1 <= f_2 <= ... <= f_n.", bold_prefix="Step 1 (Sorting): ")
    add_body("For each event i, find latest_non_conflict(i): largest index j < i where f_j <= s_i via Binary Search in O(log n).", bold_prefix="Step 2 (Binary Search): ")
    add_body(
        "DP[i] = max( DP[i - 1],   v_i + DP[latest_non_conflict(i)] )\n"
        "• Exclude event i: Max utility is DP[i - 1].\n"
        "• Include event i: Gain utility v_i plus optimal prior compatible events DP[latest_non_conflict(i)].",
        bold_prefix="Bellman Recurrence Relation: "
    )
    add_body("Time: O(n log n); Space: O(n). Result: Selects Debate, Taarangana Dance, and Moksha Star Night with 100% zero time conflicts.", bold_prefix="Complexity & Output: ")

    add_heading_2("5.2 Task 2: Department Equipment & Budget Modernization (0/1 Knapsack DP)")
    add_body(
        "Academic departments propose modernization packages (AI GPU server, robotics arena kits, digital library subscription, cleanroom testbeds). "
        "Given a total annual campus modernization budget W (e.g. ₹20 Lakhs), 0/1 Knapsack DP determines which proposals to fund to maximize total academic utility."
    )
    add_body(
        "Let DP[i, w] denote the maximum academic utility attainable using a subset of the first i proposals with budget limit w:\n"
        "DP[i, w] = (cost_i > w) ? DP[i - 1, w] : max( DP[i - 1, w],  v_i + DP[i - 1, w - cost_i] )",
        bold_prefix="0/1 Knapsack Recurrence: "
    )
    add_body("Time: O(n · W); Space: O(n · W). Output: Maximizes campus-wide impact while strictly respecting budget constraints.", bold_prefix="Complexity: ")

    # =========================================================================
    # SECTION 6: INFRASTRUCTURE OPTIMIZATION (MST)
    # =========================================================================
    add_heading_1("6. Campus Infrastructure Optimization (Kruskal & Prim MST)")
    add_body(
        "Campus administrators need to connect all 28 major landmarks with high-speed fiber-optic network cables or water pipelines with "
        "minimal trenching and installation cost. A Minimum Spanning Tree connects all 28 vertices using exactly 27 links with zero cycles."
    )

    add_heading_2("6.1 Kruskal's Algorithm (with Disjoint Set Union)")
    add_bullet("Computes pairwise walking distances between all landmark pairs using Dijkstra.", "Step 1: ")
    add_bullet("Sorts candidate edges ascending by distance in O(E log E).", "Step 2: ")
    add_bullet("Uses DSU with Path Compression (parent[i] = find(parent[i])) and Union-by-Rank. If find(u) != find(v), unites them; else rejects (avoids cycles).", "Step 3: ")
    add_bullet("Total NSUT Fiber Cable Length: 3,569 meters across 26 tree links connecting all landmarks. Estimated trenching cost: ₹16,06,050 (@ ₹450/m).", "Result: ")

    add_heading_2("6.2 Prim's Algorithm (with Min-Heap)")
    add_bullet("Starts from Admin Block (Central Server / Network Operations Center).", "Step 1: ")
    add_bullet("Greedily extracts the minimum-weight cut edge crossing from inMST to unvisited landmarks using a Min-Heap in O(E log V).", "Step 2: ")

    # =========================================================================
    # SECTION 7: VIVA VOCE QUESTIONS & MODEL ANSWERS
    # =========================================================================
    add_heading_1("7. Anticipated Viva Voce Questions & Model Answers")

    viva_qa = [
        ("Q1: What are the four core sections of the CampusNav application?",
         "The four sections are: (1) Campus Map: interactive GIS map of all 145 acres; (2) Find Route: pedestrian routing using Dijkstra, BFS, and DFS; (3) Directory: campus facilities directory powered by an AVL Tree and Hash Table; (4) Resource Allocation: festival venue scheduling via Weighted Interval Scheduling DP, budget allocation via 0/1 Knapsack DP, and utility cabling via Kruskal/Prim MST."),

        ("Q2: How is the Balanced Search Tree (AVL Tree) used in CampusNav?",
         "We implement an AVL Tree from scratch with height tracking and four balancing rotations (LL, RR, LR, RL). All 28 campus facilities are inserted alphabetically. In the Directory, facility searches execute in guaranteed O(log N) time rather than O(N) linear scans. The tree maintains a height of 6 for 28 nodes with a balance factor of -1, proving strict balance."),

        ("Q3: How is Hashing implemented and what is its role?",
         "We implement CampusHashTable with table size 37 using a Polynomial Rolling Hash (base 31) and Separate Chaining. It provides O(1) average lookup for landmarks by ID and graph adjacency access with a load factor of 0.76."),

        ("Q4: Why does Dijkstra require non-negative edge weights? Does CampusNav have negative weights?",
         "Dijkstra relies on a greedy property: once a node is popped from the priority queue, its distance is finalized. Negative weights violate this assumption. In CampusNav, all edge weights are physical Haversine ground distances (>= 0), so Dijkstra is 100% optimal."),

        ("Q5: How does Dynamic Programming solve festival venue scheduling?",
         "It models the problem as Weighted Interval Scheduling. Events are sorted by finish times. For each event i, binary search locates the latest non-conflicting event in O(log n). The Bellman recurrence DP[i] = max(DP[i-1], utility_i + DP[latest_non_conflict(i)]) evaluates whether including event i yields higher utility than excluding it, guaranteeing zero time overlaps in O(n log n)."),

        ("Q6: How does Dynamic Programming solve campus budget allocation?",
         "It uses 0/1 Knapsack DP. Given a fixed university budget W and departmental proposals with cost w_i and academic utility v_i, it builds a table DP[i, w] in O(n · W). It backtracks to output the exact set of funded proposals maximizing campus-wide impact without exceeding capacity."),

        ("Q7: How does Disjoint Set Union (DSU) prevent cycles in Kruskal's algorithm?",
         "For every candidate edge (u, v), DSU checks find(u) == find(v). If true, both nodes are already in the same connected tree, so adding the edge would form a cycle; hence it is rejected. If false, union(u, v) merges their sets in O(α(V)) amortized time."),

        ("Q8: When would you use BFS instead of Dijkstra?",
         "BFS treats all edges as having equal weight (1 hop). It minimizes the number of intermediate turns and intersections rather than metric distance. This is ideal for campus visitors who want the simplest route with fewer path decisions."),

        ("Q9: What is the purpose of DFS in your project?",
         "DFS performs deep branch exploration using a LIFO Stack. In our benchmark, it serves as an educational baseline demonstrating that unguided greedy exploration produces convoluted, suboptimal paths (2,624 m vs Dijkstra's 661 m)."),

        ("Q10: What are the time complexities of all algorithms in CampusNav?",
         "Dijkstra: O((V + E) log V); BFS: O(V + E); DFS: O(V + E); Kruskal's MST: O(E log E); Prim's MST: O(E log V); AVL Tree: O(log N) search/insert; Hash Table: O(1) average lookup; Weighted Interval Scheduling: O(n log n); 0/1 Knapsack: O(n · W).")
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
