# Smart Campus Navigation & Resource Optimizer (NSUT Dwarka)
### Data Structures & Algorithms (DSA) / Graph Theory Viva Project & Live Web System

An interactive, high-performance web application designed for **Netaji Subhas University of Technology (NSUT), Dwarka, New Delhi**. Built by mapping real-world **geospatial walking networks and building coordinates** into an optimized mathematical graph.

Deployed and hosted on **GitHub Pages**: [https://kartikkumarsingh733-rgb.github.io/Campus-Navigator/](https://kartikkumarsingh733-rgb.github.io/Campus-Navigator/)

---

## 🌟 Key Features

### 1. 🧭 3-View Modern Navigation Architecture
- **View 1: Interactive Campus Map**:
  - Interactive map with custom emoji markers, star compass, and Street/Satellite view switcher.
  - Selected Location Card (Department badge, Building, Floor, exact coordinates, description, `Set Start`, `Set Dest`).
  - Searchable, category-filtered scrollable list of all 28 campus landmarks.
- **View 2: Campus Shortest Route Finder**:
  - Route Parameters panel with Origin (including `Use My Location`), Swap button, Destination, Algorithm picker, and Turn-by-Turn Waypoint Directions.
  - Live Route Visualization map with animated dashed route polyline and path glow underlay.
- **View 3: Campus Location Directory**:
  - Complete facility catalog with live search and category filter pills (`All Locations`, `Academic`, `Hostels`, `Food & Hangouts`, `Admin`, `Landmarks`, `Sports`, `Gates`, `Utility`).
  - Responsive facility card grid with `View on Map` and `Navigate` direct actions.

### 2. 🗺️ Dual Base Map Styles
- **🗺️ Street Map**: High-clarity Carto Voyager vector raster tiles.
- **🛰️ Satellite View**: High-resolution ESRI World Imagery satellite view.

### 3. 🛰️ Real-Time HTML5 Geolocation & Live Walk Tracking
- **One-Time GPS Locate (`🎯` button & "Use My Location")**:
  - Calls `navigator.geolocation.getCurrentPosition({ enableHighAccuracy: true })`.
  - Drops a pulsing user beacon with an accuracy circle and snaps to the nearest campus walkway intersection node via Euclidean Haversine projection (`snapLocationToCampusGraph`).
- **Live GPS Walk Tracking (`🛰️` button)**:
  - Continuously streams position updates using `navigator.geolocation.watchPosition()`, re-evaluating the nearest graph node as you walk.
- **Simulate Live Walking (`▶️ Simulate Live Walking`)**:
  - Viva and indoor testing mode that animates the user marker along each waypoint of the computed route, decrementing distance (m) and walking time in real time.
- **Off-Campus Guard**:
  - Gracefully alerts users located outside campus and snaps origin to the nearest entrance gate (Main Gate 1 or North Gate 2).

### 4. 🦽 Accessible Route Preferences
- **Wheelchair & Accessible Route Toggle**: Filters out edges tagged as stairs/steps, routing solely through ramps, flat paved roads, and accessible pathways.

### 5. 🧠 Comprehensive Graph Algorithms Implemented
1. **Dijkstra's Algorithm** (with custom **Min-Heap Priority Queue**):
   - Time Complexity: $O((V + E) \log V)$
   - Guarantees the absolute shortest physical distance on weighted graphs.
2. **A\* Search Algorithm** (with **Haversine Euclidean Distance Heuristic**):
   - Directed search that prioritizes exploring nodes towards the target, expanding up to **4.5x fewer nodes** than Dijkstra while maintaining 100% optimal distance.
3. **Breadth-First Search (BFS)** (using Queue FIFO):
   - Finds the path with the minimum number of intersections/hops.
4. **Depth-First Search (DFS)** (using Stack / Backtracking):
   - Path existence and exploration comparison demonstrating sub-optimal physical distance vs Dijkstra.
5. **Kruskal's Algorithm** (with **Disjoint Set Union - DSU**, Path Compression & Union by Rank):
   - Time Complexity: $O(E \log E)$
   - Computes the **Minimum Spanning Tree (MST)** across all campus landmarks (for fiber-optic internet / water pipeline network layout).
6. **Prim's Algorithm** (with **Min-Heap**):
   - Greedily grows the MST starting from the central Admin Block.
7. **Dynamic Programming (Weighted Interval Scheduling)**:
   - Solves campus venue and hall allocation (e.g., Moksha Stage, Admin Auditorium, APJ Lecture Complex, Mini Audi) for society events without time clashes, maximizing utility.

### 6. 🧪 Live Viva Simulation Sandbox
- **Simulate Blocked Paths / Road Closures**:
  - Toggle *"Admin Fountain Corridor Closed"* or *"Moksha Ground Path Closed (Fest Setup)"* to watch the graph dynamically recalculate and reroute around blocked paths in real-time.
- **Dynamic Edge Weight Adjustments**:
  - *"Weather: Monsoon Rain"*: Applies a 2.5x penalty to unpaved/mud pathways, forcing the route onto paved, covered walkways.
  - *"Rush Hour Congestion"*: Simulates high foot-traffic congestion during class transitions around central academic choke-points.
- **Side-by-Side Algorithm Benchmark Matrix**:
  - Live side-by-side comparison table showing Distance (m), Visited Nodes, Execution Time (ms), and Optimality Guarantee.

---

## 📍 NSUT Dwarka Landmarks Included (28 Landmarks)

| Category | Landmarks |
| :--- | :--- |
| **Gates** | Main Gate (Azad Hind Fauj Marg - Gate 1), North Gate (Suraj Vihar - Gate 2) |
| **Academic** | APJ Abdul Kalam Lecture Complex, Central Library (Tagore Hub), Block 6 (COE/IT/MPAE), Block 4 (ECE), Block 5 (ICE), Smart Block, Faculty of Tech (MPC), Department of Design Block, Management Block |
| **Admin** | Admin Block (VC Office, Registrar, Main Audi), Training & Placement Cell (TnP) |
| **Hostels** | Boys' Hostels Complex (BH 1-4, Ramanujan, Aryabhatta, J.C. Bose), Kaveri Girls Hostel, Southern Girls' Hostels Complex |
| **Food & Hangouts** | Student Center & Canteen, Amul Ground & Refreshment Kiosk, Nescii Lawns (Shaheed Vatika), Moksha Festival Ground, SAC (Student Activity Centre) |
| **Sports & Health** | Sports Complex & Stadium / Running Track, Campus Clinic / Health Centre |
| **Landmarks & Utility**| Central Fountain Roundabout, Campus Mandir (Sulahkul Temple), Ecological Campus Lake, West Campus Parking, Stationery & Utility Complex, Substation & Utility Hub |

---

## 🚀 How to Deploy on GitHub Pages

This repository is already structured for zero-configuration deployment on GitHub Pages:

1. Push this codebase to your GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "feat: complete responsive NSUT campus navigation system"
   git branch -M main
   git remote add origin https://github.com/kartikkumarsingh733-rgb/Campus-Navigator.git
   git push -u origin main
   ```
2. In your GitHub repository:
   - Click **Settings** (top right of your repository page).
   - In the left sidebar, click **Pages**.
   - Under **Build and deployment** $\rightarrow$ **Source**, choose **Deploy from a branch**.
   - Under **Branch**, select `main` and folder `/ (root)`, then click **Save**.
3. Within 1–2 minutes, your live site will be active at:
   ```
   https://kartikkumarsingh733-rgb.github.io/Campus-Navigator/
   ```
4. On GitHub Pages (served via HTTPS), mobile geolocation (`Locate Me` & `Live GPS Tracking`) will be fully supported.

---

## 💻 Local Execution

Run with Python local server (enables HTML5 Geolocation on localhost):
```bash
run_app.bat
```
or
```bash
python -m http.server 8000
```
Then visit: `http://localhost:8000`

---

## 📁 File Structure

```
Campus-Navigator/
├── index.html           # Main HTML structure, 3 app views, control panels, and modals
├── styles.css           # 7-tier responsive layout, glassmorphism UI, theme variables
├── app.js               # View router, Leaflet bindings, live GPS tracking, walk simulation
├── algorithms.js        # MinHeap, DSU, Dijkstra, A*, BFS, DFS, Kruskal, Prim, DP
├── graphData.js         # Complete graph (1,409 nodes, 1,564 edges, 28 landmarks, 486 buildings)
├── leaflet.js           # Local offline Leaflet library
├── leaflet.css          # Local offline Leaflet styling
├── run_app.bat          # 1-click launcher for localhost HTTP server
├── test_algorithms.js   # Automated test suite verifying all 6 DSA algorithms
├── test_user_routes.js  # Automated test suite verifying specific campus path routes
└── README.md            # Comprehensive documentation, viva guide & deployment instructions
```

---

## 🎓 Viva Questions & Answers Cheat-Sheet

**Q1: Why did you use a Min-Heap for Dijkstra's Algorithm instead of an array?**  
*Answer:* With an unsorted array or list, extracting the minimum distance node takes $O(V)$ time, leading to an overall time complexity of $O(V^2)$. By utilizing a binary Min-Heap Priority Queue, extracting the minimum element takes $O(\log V)$, reducing the overall complexity to $O((V + E) \log V)$, which is optimal for sparse graphs like campus road networks where $E \ll V^2$.

**Q2: What is the heuristic function used in your A\* search? Is it admissible?**  
*Answer:* The heuristic $h(n)$ is the Great-Circle Haversine distance from node $n$ to the target destination. Because the straight-line/great-circle distance is always less than or equal to the actual walking path distance ($h(n) \le h^*(n)$), the heuristic never overestimates the true remaining cost. Therefore, it is **strictly admissible and consistent**, guaranteeing an optimal shortest path while expanding substantially fewer nodes (only 117 nodes vs 536 nodes for Dijkstra in our test).

**Q3: How does your tool simulate blocked roads and construction closures?**  
*Answer:* Edges in our graph have unique identifiers (`edgeId`). When a path is closed, its ID is added to a `blockedEdges` hash set. During neighbor relaxation in Dijkstra or A\*, any edge present in the set is pruned ($O(1)$ lookup), forcing the algorithm to find an alternative connected component path.

**Q4: How does Kruskal's Algorithm avoid cycles when building the MST?**  
*Answer:* It uses a **Disjoint Set Union (DSU / Union-Find)** data structure. Before adding an edge $(u, v)$ to the tree, it calls `find(u)` and `find(v)`. If both nodes belong to the same representative root, adding the edge would create a cycle, so it is skipped. Otherwise, `union(u, v)` merges the sets using union by rank and path compression in near-constant amortized time $\alpha(V)$.

**Q5: How does the Dynamic Programming Resource Optimizer work?**  
*Answer:* It solves the **Weighted Interval Scheduling Problem**. Events are sorted by finish time $O(N \log N)$. For each event $i$, we compute:
$$\text{DP}[i] = \max(\text{DP}[i-1], \text{utility}[i] + \text{DP}[\text{latestNonConflict}(i)])$$
This allows the university administration to allocate halls and stages to maximize student attendance and society utility without scheduling conflicts.

