import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_guide():
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
        hrun = hp.add_run("CampusNav • Algorithms Implementation & Viva Defense Guide")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("NSUT Dwarka • Department of Computer Science & Engineering • Viva Voce Master Guide")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)

    # Color Palette
    COLOR_PRIMARY = RGBColor(30, 58, 138)     # Deep Navy (#1E3A8A)
    COLOR_SECONDARY = RGBColor(2, 132, 199)   # Vibrant Blue / Cyan (#0284C7)
    COLOR_TEXT = RGBColor(15, 23, 42)         # Slate 900 (#0F172A)
    COLOR_MUTED = RGBColor(71, 85, 105)       # Slate 600 (#475569)
    COLOR_EMERALD = RGBColor(5, 150, 105)     # Emerald Green (#059669)
    COLOR_PURPLE = RGBColor(126, 34, 206)     # Deep Purple (#7E22CE)
    COLOR_AMBER = RGBColor(217, 119, 6)       # Amber (#D97706)

    def set_cell_background(cell, fill_hex):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def set_cell_margins(cell, top=100, bottom=100, left=130, right=130):
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

    def add_callout(text, title="KEY VIVA DEFENSE", border_color="0284C7", bg_color="F0F9FF"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.8)
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=130, bottom=130, left=170, right=170)
        
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

    def add_qa_block(question, answer, cross_q=None, cross_ans=None):
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(8)
        p_q.paragraph_format.space_after = Pt(2)
        p_q.paragraph_format.keep_with_next = True
        r_q = p_q.add_run(f"Q: {question}")
        r_q.font.name = "Arial"
        r_q.font.size = Pt(10)
        r_q.font.bold = True
        r_q.font.color.rgb = COLOR_PRIMARY

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_after = Pt(4)
        p_a.paragraph_format.left_indent = Inches(0.2)
        p_a.paragraph_format.line_spacing = 1.15
        r_lbl = p_a.add_run("Answer: ")
        r_lbl.font.bold = True
        r_lbl.font.size = Pt(9.5)
        r_a = p_a.add_run(answer)
        r_a.font.size = Pt(9.5)

        if cross_q:
            p_cq = doc.add_paragraph()
            p_cq.paragraph_format.space_before = Pt(2)
            p_cq.paragraph_format.space_after = Pt(2)
            p_cq.paragraph_format.left_indent = Inches(0.2)
            p_cq.paragraph_format.keep_with_next = True
            r_cq_lbl = p_cq.add_run("Examiner Cross-Question: ")
            r_cq_lbl.font.bold = True
            r_cq_lbl.font.size = Pt(9.5)
            r_cq_lbl.font.color.rgb = COLOR_AMBER
            r_cq = p_cq.add_run(f"\"{cross_q}\"")
            r_cq.font.italic = True
            r_cq.font.size = Pt(9.5)

            p_ca = doc.add_paragraph()
            p_ca.paragraph_format.space_after = Pt(6)
            p_ca.paragraph_format.left_indent = Inches(0.4)
            p_ca.paragraph_format.line_spacing = 1.15
            r_ca_lbl = p_ca.add_run("Defense Answer: ")
            r_ca_lbl.font.bold = True
            r_ca_lbl.font.size = Pt(9.5)
            r_ca_lbl.font.color.rgb = COLOR_EMERALD
            r_ca = p_ca.add_run(cross_ans)
            r_ca.font.size = Pt(9.5)

    # =========================================================================
    # DOCUMENT COVER & HEADER
    # =========================================================================
    add_title("CampusNav: Algorithms & Viva Defense Master Guide", 
              "Simplified Explanations, Exact Implementation Details & Viva Voce Cross-Questions")

    # Metadata Box
    meta_tbl = doc.add_table(rows=2, cols=3)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_headers = ["Institution & Campus", "Scope of Work", "Core Algorithms & Structures"]
    meta_values = [
        "Netaji Subhas University of Technology (NSUT, 145 Acres)", 
        "Ground Routing & Resource Optimization", 
        "Dijkstra, BFS, DFS, Kruskal/Prim MST, AVL Tree, Hashing, Dynamic Programming"
    ]
    for c_idx in range(3):
        c_hdr = meta_tbl.cell(0, c_idx)
        c_val = meta_tbl.cell(1, c_idx)
        set_cell_background(c_hdr, "1E3A8A")
        set_cell_background(c_val, "F8FAFC")
        set_cell_margins(c_hdr, top=80, bottom=80, left=90, right=90)
        set_cell_margins(c_val, top=80, bottom=80, left=90, right=90)
        
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

    # 30-Second Elevator Pitch
    add_callout(
        "\"CampusNav is an enterprise web navigation and resource allocation platform built for NSUT's 145-acre campus. "
        "The site is organized into four clean views: (1) Campus Map for interactive spatial exploration; (2) Find Route for shortest and "
        "fewest-turn pedestrian paths using Dijkstra, BFS, and DFS; (3) Directory for searching all 28 campus facilities in logarithmic time "
        "using a Balanced Search Tree (AVL Tree) and Custom Hash Table; and (4) Resource Allocation solving fest venue scheduling and departmental "
        "budget allocation using Dynamic Programming (Weighted Interval Scheduling and 0/1 Knapsack), plus campus fiber cabling layout using Kruskal's "
        "and Prim's Minimum Spanning Tree algorithms. All computations execute on the client side with sub-2 millisecond latency.\"",
        "30-SECOND ELEVATOR PITCH FOR YOUR PROFESSOR"
    )

    # =========================================================================
    # SECTION 1: THE 4 CORE SECTIONS OF THE SITE
    # =========================================================================
    add_heading_1("1. The 4 Core Sections of the Website")
    add_body(
        "To easily demonstrate the project to your professor, explain that the top navigation bar gives instant access to four distinct sections:"
    )

    sec_tbl = doc.add_table(rows=5, cols=4)
    sec_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_headers = ["Section Name", "Where on Site", "What the User Does", "Algorithms / DSA Powering It"]
    s_data = [
        ["1. Campus Map", "Navbar Tab 1 (#view-campus-map)", "Views 145-acre NSUT satellite/street map, clicks 28 facility pill markers, inspects details.", "Leaflet.js GIS, WGS-84 coordinates, Spatial Snapping."],
        ["2. Find Route", "Navbar Tab 2 (#view-find-route)", "Selects Start and Destination, picks Dijkstra / BFS / DFS, toggles wheelchair accessibility, views live route.", "Dijkstra (Min-Heap), BFS (Queue), DFS (Stack)."],
        ["3. Directory", "Navbar Tab 3 (#view-directory)", "Searches campus blocks with live autocomplete and filters by category (Academic, Hostels, etc.).", "Balanced Search Tree (AVL Tree with O(log N) prefix search) & Custom Hash Table (O(1))."],
        ["4. Resource Allocation", "Navbar Tab 4 (#view-resource-allocation)", "Executes fest venue scheduling, lab budget modernization, and campus fiber cabling layout.", "Dynamic Programming (Weighted Interval Scheduling & 0/1 Knapsack) + MST (Kruskal & Prim)."]
    ]
    for c_i, h_text in enumerate(s_headers):
        c = sec_tbl.cell(0, c_i)
        set_cell_background(c, "1E3A8A")
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_i, r_data in enumerate(s_data):
        for c_i, val in enumerate(r_data):
            c = sec_tbl.cell(r_i + 1, c_i)
            bg = "F0F9FF" if r_i % 2 == 1 else "FFFFFF"
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=70, right=70)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_i == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_PRIMARY

    p_spacer_sec = doc.add_paragraph()
    p_spacer_sec.paragraph_format.space_after = Pt(8)

    # =========================================================================
    # SECTION 2: DIJKSTRA'S ALGORITHM
    # =========================================================================
    add_heading_1("2. Dijkstra's Algorithm (Guaranteed Shortest Metric Path)")
    
    add_heading_2("Simplified Explanation (How to explain to professor):")
    add_body(
        "\"Dijkstra's algorithm is a greedy algorithm that finds the shortest physical path from a starting node to all other nodes on a weighted graph. "
        "It maintains a priority queue of unvisited nodes ordered by distance from the origin. In each step, it extracts the node with the minimum tentative "
        "distance, visits its neighbors, and updates ('relaxes') their distances if a shorter path through the current node is discovered. "
        "Once a node is finalized, its shortest distance is mathematically guaranteed.\""
    )

    add_heading_2("Where it is used on our site:")
    add_bullet("Inside the Find Route section. It is the default algorithm chip ('Dijkstra (Heap)').", "UI Location: ")
    add_bullet("Called in app.js via algos.runDijkstra(adjacency, startNode, endNode, nodes, options) when the user clicks 'Find Shortest Route'.", "Code Invocation: ")
    add_bullet("Outputs the exact metric distance (e.g. 661 m from Main Gate to APJ Complex), computes walk time (8 min), and draws the glowing route polyline on the map.", "User Output: ")

    add_heading_2("Exact Implementation Details:")
    add_bullet("Uses our custom Binary Min-Heap class (algorithms.js lines 7–71). Push and Pop operate in O(log V) time.", "Data Structure: ")
    add_bullet("Time Complexity: O((V + E) log V); Space Complexity: O(V).", "Complexity: ")
    add_bullet("Early-Exit Optimization: As soon as u === endNode is popped from the min-heap, the loop terminates immediately without exploring the rest of the campus.", "Optimization: ")
    add_bullet("Accessibility: If the user toggles 'Wheelchair / Accessible', the algorithm bypasses edges with edge.type === 'steps', finding a 100% ramp-friendly path.", "Special Feature: ")

    add_heading_2("Viva Questions & Examiner Cross-Questions:")
    add_qa_block(
        "Why did you use Dijkstra instead of just using Euclidean straight-line distance?",
        "Euclidean distance assumes an open, unobstructed flat plane ('as the crow flies'). In reality, pedestrians must follow physical footpaths, paved roads, and indoor breezeways around academic blocks, buildings, and lawns. Dijkstra finds the true navigable path through surveyed footpath edges.",
        "Can Dijkstra handle negative edge weights? Does your project have negative weights?",
        "No, Dijkstra cannot handle negative weights because its greedy assumption—that once a node is popped its distance is finalized—would be violated if a negative edge later reduced that distance. However, in our campus graph, edge weights represent physical ground distances in meters (which are strictly >= 0), so Dijkstra is 100% guaranteed to be optimal."
    )
    add_qa_block(
        "Why implement a custom Min-Heap instead of JavaScript's built-in array.sort()?",
        "Calling array.sort() on every iteration takes O(K log K) where K is the number of open frontier nodes, degrading overall Dijkstra performance to O(V · K log K). A custom Binary Min-Heap provides O(log V) insertion and extraction, ensuring optimal O((V + E) log V) runtime."
    )

    # =========================================================================
    # SECTION 3: BREADTH-FIRST SEARCH (BFS)
    # =========================================================================
    add_heading_1("3. Breadth-First Search (BFS - Fewest Turns & Hops)")

    add_heading_2("Simplified Explanation:")
    add_body(
        "\"BFS explores vertices radially, level by level, like ripples spreading in water. It treats all edges as having uniform weight (1 hop). "
        "While Dijkstra minimizes physical meters, BFS minimizes the number of road intersections and turns. This gives campus visitors a route with the simplest navigation decisions.\""
    )

    add_heading_2("Where it is used on our site:")
    add_bullet("Find Route section under the algorithm chip 'BFS (Hops)'. Also compared inside the 'Compare All Algorithms' benchmark table.", "UI Location: ")
    add_bullet("Called via algos.runBFS(adjacency, startNode, endNode, nodes, options) in app.js.", "Code Invocation: ")
    add_bullet("Outputs total distance (690 m) and minimum intersection turns (22 hops from Main Gate to APJ Complex).", "User Output: ")

    add_heading_2("Exact Implementation Details:")
    add_bullet("Uses a FIFO Queue (queue.shift() and queue.push()) and a visited Set.", "Data Structure: ")
    add_bullet("Time Complexity: O(V + E); Space Complexity: O(V).", "Complexity: ")
    add_bullet("Offline Graph Audit: Used in build_graph.py to verify that all 1,409 nodes form a single connected component with zero unreachable islands.", "Additional Role: ")

    add_heading_2("Viva Questions & Examiner Cross-Questions:")
    add_qa_block(
        "Why does BFS guarantee the shortest path in unweighted graphs, but not in weighted graphs?",
        "In an unweighted graph, each edge costs 1 unit. When BFS explores level by level, the first time it reaches a vertex, it is guaranteed to be via the fewest number of edges. But on a weighted graph, a path with 2 long edges (e.g. 500m + 500m = 1000m) has fewer hops than a path with 3 short edges (e.g. 100m + 100m + 100m = 300m). BFS chooses the 1000m path because it has fewer hops, whereas Dijkstra correctly chooses the 300m path.",
        "When would a student or visitor prefer the BFS route over the Dijkstra route?",
        "When navigating an unfamiliar campus, fewer turns mean fewer opportunities to take a wrong fork in the road. BFS gives the route with the fewest navigational decision points (turns/intersections)."
    )

    # =========================================================================
    # SECTION 4: DEPTH-FIRST SEARCH (DFS)
    # =========================================================================
    add_heading_1("4. Depth-First Search (DFS - Deep Path Traversal)")

    add_heading_2("Simplified Explanation:")
    add_body(
        "\"DFS explores as deeply as possible along each branch before backtracking. In CampusNav, DFS is implemented as an educational benchmark "
        "to demonstrate to students and examiners why unguided graph traversal fails for spatial navigation: because it has no sense of direction or distance, "
        "it wanders through long detour loops before arriving at the destination.\""
    )

    add_heading_2("Where it is used on our site:")
    add_bullet("Find Route section under algorithm chip 'DFS (Path)', and in the Algorithm Benchmark modal.", "UI Location: ")
    add_bullet("Called via algos.runDFS(...) in app.js.", "Code Invocation: ")
    add_bullet("Produces a path of 2,624 meters and 95 hops (compared to Dijkstra's 661 meters and 22 hops).", "User Output: ")

    add_heading_2("Exact Implementation Details:")
    add_bullet("Uses an explicit LIFO Stack (stack.pop() and stack.push()) and a visited Set.", "Data Structure: ")
    add_bullet("Time Complexity: O(V + E); Space Complexity: O(V).", "Complexity: ")

    add_heading_2("Viva Questions & Examiner Cross-Questions:")
    add_qa_block(
        "Why is DFS path so much longer than Dijkstra or BFS?",
        "DFS dives blindly down the first available neighbor edge at every junction. If it encounters a side path leading all the way around the sports complex or residential quarters, it explores that entire sub-branch to the end before backtracking. It has zero cost guidance, leading to massive detours.",
        "If DFS is bad for shortest paths, what is it actually good for in computer science?",
        "DFS is fundamental for topological sorting (task scheduling), detecting cycles in directed graphs, finding connected components, solving mazes, and analyzing strongly connected components via Kosaraju's or Tarjan's algorithm."
    )

    # =========================================================================
    # SECTION 5: MINIMUM SPANNING TREE (KRUSKAL & PRIM)
    # =========================================================================
    add_heading_1("5. Minimum Spanning Tree (MST - Kruskal's & Prim's Algorithms)")

    add_heading_2("Simplified Explanation:")
    add_body(
        "\"A Spanning Tree is a subset of graph edges that connects all vertices together with zero cycles. A Minimum Spanning Tree (MST) is the spanning tree "
        "with the minimum possible total edge weight. In CampusNav, it solves a real administrative problem: connecting all 28 major campus landmarks "
        "with high-speed fiber-optic internet cables or water pipelines with the lowest possible cabling and trenching cost.\""
    )

    add_heading_2("Where it is used on our site:")
    add_bullet("Inside the Resource Allocation section under Task 3 ('Infrastructure Cabling Layout').", "UI Location: ")
    add_bullet("Two interactive buttons: 'Run Kruskal's (DSU)' and 'Run Prim's (Min-Heap)'.", "Controls: ")
    add_bullet("Displays total cable length (3,569 m), estimated installation cost (₹16,06,050 @ ₹450/m), and the 26 individual tree links in an interactive table.", "User Output: ")

    add_heading_2("Exact Implementation Details:")
    add_bullet(
        "Edge-centric. Precomputes candidate shortest paths between landmarks via Dijkstra. "
        "Sorts all candidate edges in ascending order of distance in O(E log E). "
        "Iterates through sorted edges and uses Disjoint Set Union (DSU) to check find(u) == find(v). "
        "If distinct, calls union(u, v) and adds to MST; if already in same set, discards to avoid cycles. Halts when |V| - 1 edges are added.",
        "Kruskal's Algorithm: "
    )
    add_bullet(
        "Vertex-centric. Starts with Admin Block (Central NOC) in inMST set. Pushes incident edges crossing the cut into a Min-Heap. "
        "Greedily extracts the minimum-weight cut edge, adds the new landmark to inMST, and repeats until all 28 landmarks are spanned (Time: O(E log V)).",
        "Prim's Algorithm: "
    )
    add_bullet(
        "DSU class (algorithms.js lines 77–116) implements Path Compression (parent[i] = find(parent[i])) and Union-by-Rank. "
        "This achieves O(α(V)) amortized time per operation, where α is the inverse Ackermann function (effectively O(1) in practice).",
        "DSU Optimization: "
    )

    add_heading_2("Viva Questions & Examiner Cross-Questions:")
    add_qa_block(
        "What is the difference between Dijkstra and Prim's algorithm? Both use a Min-Heap!",
        "This is a classic examiner trap! Dijkstra's priority is g(n) = the total accumulated distance from the START node to node n. Prim's priority is simply the weight of the single edge connecting node n to the growing MST tree, regardless of distance to the start. Dijkstra builds a shortest-path tree rooted at one origin; Prim builds a global minimum weight spanning tree.",
        "When is Kruskal preferred over Prim?",
        "Kruskal is preferred on sparse graphs (E ≈ V) because sorting fewer edges is very fast. Prim is preferred on dense graphs (E ≈ V^2) when implemented with an adjacency matrix or Fibonacci heap."
    )

    # =========================================================================
    # SECTION 6: BALANCED SEARCH TREE (AVL TREE)
    # =========================================================================
    add_heading_1("6. Balanced Search Tree: Self-Balancing AVL Tree")

    add_heading_2("Simplified Explanation:")
    add_body(
        "\"A standard Binary Search Tree (BST) can become skewed like a linked list if keys are inserted in sorted order, degrading search time from "
        "O(log N) to O(N). An AVL Tree is a Self-Balancing Binary Search Tree that guarantees strict balance: for every single node, the height difference "
        "between its left and right subtrees (Balance Factor) can never exceed 1. If an insertion causes an imbalance, it performs self-adjusting tree rotations "
        "to restore balance in O(1) time.\""
    )

    add_heading_2("Where it is used on our site:")
    add_bullet("Inside the Campus Directory section (Navbar Tab 3: #view-directory).", "UI Location: ")
    add_bullet("Indexes all 28 campus facilities alphabetically by name upon app initialization (landmarkAVLTree = new algos.AVLTree()).", "Code Invocation: ")
    add_bullet("When a user types in the directory search bar, landmarkAVLTree.searchPrefix(query) executes in O(log N) time to find matching facilities.", "Functionality: ")
    add_bullet("Live status badge displayed in the directory: 'AVL Tree Height: 6 | Balanced (Yes) | Hash Table: 28 keys'.", "Visual Inspection: ")

    add_heading_2("Exact Implementation Details:")
    add_bullet("AVLNode class tracks key, value, height, left, and right child pointers.", "Node Structure: ")
    add_bullet("Balance Factor: getBalanceFactor(node) = getHeight(node.left) - getHeight(node.right). Must be in {-1, 0, 1}.", "Balance Invariant: ")
    add_bullet("Left-Left (LL) Imbalance: Resolved by single rotateRight(node).", "Rotation 1: ")
    add_bullet("Right-Right (RR) Imbalance: Resolved by single rotateLeft(node).", "Rotation 2: ")
    add_bullet("Left-Right (LR) Imbalance: Resolved by rotateLeft(node.left) followed by rotateRight(node).", "Rotation 3: ")
    add_bullet("Right-Left (RL) Imbalance: Resolved by rotateRight(node.right) followed by rotateLeft(node).", "Rotation 4: ")
    add_bullet("Complexity: Search, Insert, and Delete are strictly O(log N) in both average and worst cases.", "Complexity: ")

    add_heading_2("Viva Questions & Examiner Cross-Questions:")
    add_qa_block(
        "Why use an AVL Tree instead of a simple JavaScript Array.filter() in the Directory?",
        "Array.filter() performs an O(N) linear scan across every element. For small datasets it works, but it does not scale. An AVL Tree organizes data into a balanced logarithmic hierarchy, guaranteeing O(log N) search time even if the university directory grows to thousands of faculty offices, classrooms, and labs.",
        "What is the difference between an AVL Tree and a Red-Black Tree?",
        "AVL Trees are more rigidly balanced than Red-Black trees (height difference strictly <= 1 vs <= 2x). Therefore, AVL trees provide faster lookups/search operations (fewer tree levels), making them ideal for search-intensive applications like our campus directory. Red-Black trees require fewer rotations during frequent insertions and deletions."
    )

    # =========================================================================
    # SECTION 7: CUSTOM HASHING (CAMPUSHASHTABLE)
    # =========================================================================
    add_heading_1("7. Custom Hashing (CampusHashTable with Separate Chaining)")

    add_heading_2("Simplified Explanation:")
    add_body(
        "\"Hashing maps arbitrary string keys (like 'main_gate' or 'admin_block') to numerical indices in an array using a mathematical hash function. "
        "This allows instant O(1) data retrieval without searching through items one by one. If two keys hash to the same bucket index (a collision), "
        "our hash table stores them in a linked bucket list (Separate Chaining).\""
    )

    add_heading_2("Where it is used on our site:")
    add_bullet("Throughout the application for instant O(1) lookup of landmarks by ID (landmarkHashTable.get('apj_complex')) and graph adjacency lookups.", "Where on Site: ")
    add_bullet("Implemented in algorithms.js lines 122–215 as CampusHashTable.", "Code Location: ")

    add_heading_2("Exact Implementation Details:")
    add_bullet("Fixed array of 37 buckets (37 is prime, which reduces clustering and harmonic collisions).", "Bucket Array: ")
    add_bullet("Polynomial Rolling Hash: hash(str) = sum(str.charCodeAt(i) * 31^(len-1-i)) mod 37.", "Hash Function: ")
    add_bullet("Collision Handling: Separate Chaining (bucket arrays).", "Collision Method: ")
    add_bullet("Load Factor: α = N / M = 28 / 37 ≈ 0.76 (optimal balance between memory usage and collision minimization).", "Load Factor: ")
    add_bullet("Complexity: O(1) average lookup, insertion, and deletion; O(N) worst case if all keys hash to a single bucket.", "Complexity: ")

    add_heading_2("Viva Questions & Examiner Cross-Questions:")
    add_qa_block(
        "Why did you choose prime number 37 for the hash table bucket size?",
        "If the table size is a composite number sharing factors with the key data or multiplier (31), keys will cluster in specific bucket multiples, causing severe collisions. Choosing a prime number coprime to the base ensures that the polynomial rolling hash values distribute uniformly across all buckets.",
        "What is the difference between Separate Chaining and Open Addressing?",
        "In Separate Chaining, each bucket points to an auxiliary list where colliding items are appended; the table can hold more items than its bucket capacity (load factor can exceed 1). In Open Addressing (e.g. Linear Probing), all elements stay inside the array; collisions probe subsequent empty slots, and performance collapses when the table approaches 80% full."
    )

    # =========================================================================
    # SECTION 8: DYNAMIC PROGRAMMING (RESOURCE ALLOCATION)
    # =========================================================================
    add_heading_1("8. Dynamic Programming for Campus Resource Allocation")

    add_heading_2("Task 1: Fest Venue & Event Allocation (Weighted Interval Scheduling)")
    add_body(
        "\"During college fests (Moksha, Taarangana), multiple student societies request prestigious venues (Admin Audi, APJ Complex, Moksha Ground) "
        "with overlapping start and end times and varying student impact scores. Standard greedy interval scheduling only works when all events have equal value. "
        "When events have utility weights, only Dynamic Programming guarantees the global maximum utility without any time overlaps.\""
    )
    add_bullet("Resource Allocation section under Tab 1 ('1. Fest & Venue Scheduling'). Button: 'Run DP Interval Scheduling'.", "Where on Site: ")
    add_bullet("Step 1: Sort all events by finish time f_1 <= f_2 <= ... <= f_n.", "Algorithm Step 1: ")
    add_bullet("Step 2: For each event i, find latest_non_conflict(i): the largest index j < i such that f_j <= s_i using Binary Search in O(log N).", "Algorithm Step 2: ")
    add_bullet("Step 3: Bellman Recurrence: DP[i] = max( DP[i - 1],   utility_i + DP[latest_non_conflict(i)] ).", "Algorithm Step 3: ")
    add_bullet("Time Complexity: O(N log N); Space Complexity: O(N).", "Complexity: ")
    add_bullet("Result: Approves 3 non-conflicting events (Debate, Taarangana Dance, Moksha EDM Night) achieving a maximum 245 utility points.", "Site Output: ")

    add_heading_2("Task 2: Department Equipment & Modernization Budget (0/1 Knapsack DP)")
    add_body(
        "\"University administrators receive modernization funding proposals from academic departments (AI GPU cluster, robotics testbeds, library subscriptions). "
        "Given a fixed annual campus modernization budget W (e.g. ₹20 Lakhs), 0/1 Knapsack DP determines the exact subset of proposals to fund to maximize academic utility.\""
    )
    add_bullet("Resource Allocation section under Tab 2 ('2. Budget & Lab Equipment'). User can choose budget (₹15L, ₹20L, ₹25L, ₹30L).", "Where on Site: ")
    add_bullet("Recurrence: DP[i, w] = (cost_i > w) ? DP[i-1, w] : max( DP[i-1, w],  utility_i + DP[i-1, w - cost_i] ).", "Recurrence: ")
    add_bullet("Time Complexity: O(N · W); Space Complexity: O(N · W). Backtracks through table to output funded vs rejected proposals.", "Complexity: ")

    add_heading_2("Viva Questions & Examiner Cross-Questions:")
    add_qa_block(
        "Why can't we use a Greedy approach (like sorting by utility/cost ratio) for 0/1 Knapsack?",
        "Greedy sorting by value-to-weight ratio only works for the Fractional Knapsack problem (where items can be split into fractions, like grain). For 0/1 Knapsack, an item must be chosen completely or not at all. A greedy choice can consume capacity with a high-ratio item and leave insufficient space for a combination of items that together would yield far higher total utility. Dynamic Programming explores all overlapping subproblems to guarantee the true global optimum.",
        "Why is 0/1 Knapsack considered pseudo-polynomial time?",
        "The runtime is O(N · W). W is the numerical value of the capacity, not the number of input items. If W is represented in binary, its input length is log2(W) bits. Since the time is exponential with respect to the number of bits in W, it is classified as pseudo-polynomial (polynomial in numerical value, but exponential in bit length)."
    )

    # =========================================================================
    # SECTION 9: 20 RAPID-FIRE VIVA DEFENSE QUESTIONS
    # =========================================================================
    add_heading_1("9. Top 20 Rapid-Fire Viva Defense Questions & Answers")

    cheat_sheet = [
        ("Q1: What graph representation is used in CampusNav?", 
         "An Adjacency List (Hash Map of nodeId -> Array of Edge objects) storing 1,409 nodes and 1,564 edges in O(V + E) space."),
        
        ("Q2: How are edge weights calculated in your campus graph?", 
         "Using the Haversine great-circle formula over the WGS-84 Earth sphere (R = 6,371,000 m) to give exact physical metric meters."),
        
        ("Q3: How do you handle GPS inaccuracy when a student clicks 'Use My Location'?", 
         "Spatial Snapping computes the Haversine distance from the GPS coordinate to all 1,409 nodes, snapping the user to the nearest walkable junction node V_snap in O(V) time."),
        
        ("Q4: What is the time complexity of Dijkstra with a Min-Heap?", 
         "O((V + E) log V). Extracting min-distance takes O(log V) and each of the E edges is relaxed at most once."),
        
        ("Q5: What is early-exit in Dijkstra?", 
         "Terminating the while-loop as soon as the destination vertex is popped from the priority queue, avoiding exploring the rest of the campus."),
        
        ("Q6: How is wheelchair accessibility implemented?", 
         "Each edge carries a boolean flag. If accessibility is enabled, edges tagged with type === 'steps' are bypassed during neighbor relaxation, routing strictly along ramps."),
        
        ("Q7: How does BFS ensure the fewest turns?", 
         "BFS explores by unweighted edge hops. Treating each edge as 1 unit guarantees finding the path with the minimum number of intersections/decision points."),
        
        ("Q8: Why is DFS unsuitable for shortest paths?", 
         "DFS dives deeply down the first available branch without cost guidance, producing highly suboptimal detours (e.g. 2,624 m vs 661 m)."),
        
        ("Q9: What is a Minimum Spanning Tree (MST)?", 
         "A subset of edges that connects all V vertices with zero cycles while minimizing the sum of edge weights."),
        
        ("Q10: What is the total length of your campus fiber-optic MST?", 
         "3,569 meters across 26 tree links connecting all 28 major NSUT landmarks."),
        
        ("Q11: How does DSU prevent cycles in Kruskal's algorithm?", 
         "For each edge (u, v), it checks find(u) == find(v). If true, both vertices are already in the same connected tree, so adding the edge would form a cycle; hence it is rejected."),
        
        ("Q12: What optimizations are in your DSU implementation?", 
         "Path Compression (parent flattens to root during find) and Union by Rank (smaller tree attached under larger), giving O(α(V)) amortized time."),
        
        ("Q13: How does Prim's algorithm expand the tree?", 
         "It starts with Admin Block in the tree and uses a Min-Heap to greedily pick the minimum-weight cut edge connecting a tree vertex to an unvisited landmark."),
        
        ("Q14: What is an AVL Tree and why is it used?", 
         "A Self-Balancing Binary Search Tree where the Balance Factor (left height - right height) is strictly in {-1, 0, 1}. Used in Directory for O(log N) facility lookups."),
        
        ("Q15: What are the 4 rotation cases in an AVL Tree?", 
         "Left-Left (single right rotation), Right-Right (single left rotation), Left-Right (left rotation on child then right on node), and Right-Left (right rotation on child then left on node)."),
        
        ("Q16: How does the Directory search use the AVL Tree?", 
         "When a user types a prefix, it queries the AVL Tree via searchPrefix(query) in O(log N) time rather than doing an O(N) linear array scan."),
        
        ("Q17: How is Hashing implemented in your project?", 
         "CampusHashTable uses a 37-bucket array, Polynomial Rolling Hash with base 31, and Separate Chaining to provide O(1) average landmark lookup."),
        
        ("Q18: What is Weighted Interval Scheduling and why use DP?", 
         "It schedules non-overlapping events with start/finish times and utility scores. Greedy sorting fails because high-utility events may be rejected; DP evaluates all combinations in O(N log N)."),
        
        ("Q19: What is 0/1 Knapsack and how is it used in your site?", 
         "It maximizes departmental utility within a fixed modernization budget W. It builds a DP table in O(N · W) and backtracks to output funded proposals."),
        
        ("Q20: Why does the entire CampusNav application run on the client side?", 
         "Bundling graph data and algorithms in JavaScript eliminates server hosting latency, API rate limits, and network round-trips, executing routing in under 2 milliseconds with offline capability.")
    ]

    for q, a in cheat_sheet:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r_q = p.add_run(f"• {q}\n")
        r_q.font.name = "Arial"
        r_q.font.size = Pt(9.5)
        r_q.font.bold = True
        r_q.font.color.rgb = COLOR_PRIMARY
        r_a = p.add_run(f"   {a}")
        r_a.font.name = "Calibri"
        r_a.font.size = Pt(9)
        r_a.font.color.rgb = COLOR_TEXT

    # Save
    doc.save("CampusNav_Algorithms_and_Viva_Guide.docx")
    print("Document successfully created: CampusNav_Algorithms_and_Viva_Guide.docx")

if __name__ == "__main__":
    create_guide()
