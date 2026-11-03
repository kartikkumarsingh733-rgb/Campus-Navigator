// NSUT Dwarka Smart Campus Navigation & Resource Optimizer
// Core Data Structures & Graph Algorithms
// Allowed Algorithms: BFS, DFS, Dijkstra, MST (Kruskal/Prim), Balanced Search Tree (AVL), Hashing, Dynamic Programming

// -------------------------------------------------------------
// 1. Min-Heap Priority Queue (Data Structure for Dijkstra & Prim)
// -------------------------------------------------------------
class MinHeap {
  constructor() {
    this.heap = [];
  }

  push(item) {
    this.heap.push(item);
    this._bubbleUp(this.heap.length - 1);
  }

  pop() {
    if (this.isEmpty()) return null;
    const min = this.heap[0];
    const end = this.heap.pop();
    if (this.heap.length > 0) {
      this.heap[0] = end;
      this._sinkDown(0);
    }
    return min;
  }

  isEmpty() {
    return this.heap.length === 0;
  }

  _bubbleUp(index) {
    const element = this.heap[index];
    while (index > 0) {
      const parentIdx = Math.floor((index - 1) / 2);
      const parent = this.heap[parentIdx];
      if (element.priority >= parent.priority) break;
      this.heap[index] = parent;
      this.heap[parentIdx] = element;
      index = parentIdx;
    }
  }

  _sinkDown(index) {
    const length = this.heap.length;
    const element = this.heap[index];
    while (true) {
      let leftChildIdx = 2 * index + 1;
      let rightChildIdx = 2 * index + 2;
      let swapIdx = null;

      if (leftChildIdx < length) {
        if (this.heap[leftChildIdx].priority < element.priority) {
          swapIdx = leftChildIdx;
        }
      }

      if (rightChildIdx < length) {
        const leftPriority = swapIdx === null ? element.priority : this.heap[leftChildIdx].priority;
        if (this.heap[rightChildIdx].priority < leftPriority) {
          swapIdx = rightChildIdx;
        }
      }

      if (swapIdx === null) break;
      this.heap[index] = this.heap[swapIdx];
      this.heap[swapIdx] = element;
      index = swapIdx;
    }
  }
}

// -------------------------------------------------------------
// 2. Disjoint Set Union (DSU) with Path Compression & Union by Rank
// (Data Structure for Kruskal's MST)
// -------------------------------------------------------------
class DSU {
  constructor(elements) {
    this.parent = {};
    this.rank = {};
    for (const el of elements) {
      this.parent[el] = el;
      this.rank[el] = 0;
    }
  }

  find(i) {
    if (this.parent[i] === undefined) {
      this.parent[i] = i;
      this.rank[i] = 0;
      return i;
    }
    if (this.parent[i] !== i) {
      this.parent[i] = this.find(this.parent[i]); // Path compression: O(1) amortized
    }
    return this.parent[i];
  }

  union(i, j) {
    const rootI = this.find(i);
    const rootJ = this.find(j);
    if (rootI !== rootJ) {
      // Union by rank
      if (this.rank[rootI] < this.rank[rootJ]) {
        this.parent[rootI] = rootJ;
      } else if (this.rank[rootI] > this.rank[rootJ]) {
        this.parent[rootJ] = rootI;
      } else {
        this.parent[rootJ] = rootI;
        this.rank[rootI]++;
      }
      return true;
    }
    return false;
  }
}

// -------------------------------------------------------------
// 3. Custom Hash Table with Polynomial Rolling Hash & Separate Chaining
// (Data Structure: Hashing for O(1) Landmark & Graph Lookups)
// -------------------------------------------------------------
class CampusHashTable {
  constructor(size = 37) {
    this.size = size;
    this.buckets = new Array(size).fill(null).map(() => []);
    this.count = 0;
  }

  _hash(key) {
    const str = String(key);
    let hash = 0;
    const prime = 31;
    for (let i = 0; i < str.length; i++) {
      hash = (hash * prime + str.charCodeAt(i)) % this.size;
    }
    return Math.abs(hash);
  }

  set(key, value) {
    const idx = this._hash(key);
    const bucket = this.buckets[idx];
    for (let i = 0; i < bucket.length; i++) {
      if (bucket[i].key === key) {
        bucket[i].value = value;
        return;
      }
    }
    bucket.push({ key, value });
    this.count++;
  }

  get(key) {
    const idx = this._hash(key);
    const bucket = this.buckets[idx];
    for (let i = 0; i < bucket.length; i++) {
      if (bucket[i].key === key) {
        return bucket[i].value;
      }
    }
    return undefined;
  }

  has(key) {
    return this.get(key) !== undefined;
  }

  delete(key) {
    const idx = this._hash(key);
    const bucket = this.buckets[idx];
    for (let i = 0; i < bucket.length; i++) {
      if (bucket[i].key === key) {
        bucket.splice(i, 1);
        this.count--;
        return true;
      }
    }
    return false;
  }

  keys() {
    const result = [];
    for (const bucket of this.buckets) {
      for (const entry of bucket) {
        result.push(entry.key);
      }
    }
    return result;
  }

  values() {
    const result = [];
    for (const bucket of this.buckets) {
      for (const entry of bucket) {
        result.push(entry.value);
      }
    }
    return result;
  }

  stats() {
    let emptyBuckets = 0;
    let maxCollisions = 0;
    for (const bucket of this.buckets) {
      if (bucket.length === 0) emptyBuckets++;
      if (bucket.length > maxCollisions) maxCollisions = bucket.length;
    }
    return {
      totalKeys: this.count,
      tableSize: this.size,
      loadFactor: parseFloat((this.count / this.size).toFixed(2)),
      emptyBuckets,
      maxCollisions
    };
  }
}

// -------------------------------------------------------------
// 4. Balanced Search Tree: AVL Tree with Rotations (O(log N) Search)
// (Data Structure: Balanced Search Tree for Directory & Landmark Indexing)
// -------------------------------------------------------------
class AVLNode {
  constructor(key, value) {
    this.key = key;           // Lexicographical sorting key (e.g. facility name)
    this.value = value;       // Facility object metadata
    this.height = 1;
    this.left = null;
    this.right = null;
  }
}

class AVLTree {
  constructor() {
    this.root = null;
    this.size = 0;
  }

  getHeight(node) {
    return node ? node.height : 0;
  }

  getBalanceFactor(node) {
    return node ? this.getHeight(node.left) - this.getHeight(node.right) : 0;
  }

  updateHeight(node) {
    if (node) {
      node.height = 1 + Math.max(this.getHeight(node.left), this.getHeight(node.right));
    }
  }

  // Right Rotation (LL Imbalance)
  rotateRight(y) {
    const x = y.left;
    const T2 = x.right;

    x.right = y;
    y.left = T2;

    this.updateHeight(y);
    this.updateHeight(x);

    return x;
  }

  // Left Rotation (RR Imbalance)
  rotateLeft(x) {
    const y = x.right;
    const T2 = y.left;

    y.left = x;
    x.right = T2;

    this.updateHeight(x);
    this.updateHeight(y);

    return y;
  }

  insert(key, value) {
    const _insert = (node, k, v) => {
      if (!node) {
        this.size++;
        return new AVLNode(k, v);
      }

      if (k < node.key) {
        node.left = _insert(node.left, k, v);
      } else if (k > node.key) {
        node.right = _insert(node.right, k, v);
      } else {
        node.value = v; // Update existing
        return node;
      }

      this.updateHeight(node);
      const balance = this.getBalanceFactor(node);

      // Case 1: Left-Left
      if (balance > 1 && k < node.left.key) {
        return this.rotateRight(node);
      }
      // Case 2: Right-Right
      if (balance < -1 && k > node.right.key) {
        return this.rotateLeft(node);
      }
      // Case 3: Left-Right
      if (balance > 1 && k > node.left.key) {
        node.left = this.rotateLeft(node.left);
        return this.rotateRight(node);
      }
      // Case 4: Right-Left
      if (balance < -1 && k < node.right.key) {
        node.right = this.rotateRight(node.right);
        return this.rotateLeft(node);
      }

      return node;
    };

    this.root = _insert(this.root, key, value);
  }

  search(key) {
    let curr = this.root;
    while (curr) {
      if (key === curr.key) return curr.value;
      if (key < curr.key) curr = curr.left;
      else curr = curr.right;
    }
    return null;
  }

  // Prefix matching search (e.g. for autocomplete in directory)
  searchPrefix(prefix) {
    const p = prefix.toLowerCase();
    const matches = [];
    const _traverse = (node) => {
      if (!node) return;
      if (node.key.toLowerCase().startsWith(p) || (node.value && node.value.name && node.value.name.toLowerCase().includes(p))) {
        matches.push(node.value);
      }
      _traverse(node.left);
      _traverse(node.right);
    };
    _traverse(this.root);
    return matches;
  }

  inOrderTraversal() {
    const result = [];
    const _inOrder = (node) => {
      if (!node) return;
      _inOrder(node.left);
      result.push({ key: node.key, value: node.value, height: node.height });
      _inOrder(node.right);
    };
    _inOrder(this.root);
    return result;
  }

  rangeSearch(low, high) {
    const result = [];
    const _range = (node) => {
      if (!node) return;
      if (low < node.key) _range(node.left);
      if (low <= node.key && node.key <= high) {
        result.push(node.value);
      }
      if (high > node.key) _range(node.right);
    };
    _range(this.root);
    return result;
  }

  getTreeStats() {
    return {
      size: this.size,
      height: this.getHeight(this.root),
      rootKey: this.root ? this.root.key : null,
      balanceFactor: this.getBalanceFactor(this.root),
      isBalanced: Math.abs(this.getBalanceFactor(this.root)) <= 1
    };
  }
}

// -------------------------------------------------------------
// Helper: Haversine distance between two [lat, lon] coordinates (in meters)
// -------------------------------------------------------------
function haversineDistance(c1, c2) {
  const R = 6371000;
  const rad = Math.PI / 180;
  const dLat = (c2[0] - c1[0]) * rad;
  const dLon = (c2[1] - c1[1]) * rad;
  const lat1 = c1[0] * rad;
  const lat2 = c2[0] * rad;

  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

// -------------------------------------------------------------
// Helper: Calculate Bearing (Angle in degrees for Turn Directions)
// -------------------------------------------------------------
function calculateBearing(p1, p2) {
  const rad = Math.PI / 180;
  const lat1 = p1[0] * rad;
  const lon1 = p1[1] * rad;
  const lat2 = p2[0] * rad;
  const lon2 = p2[1] * rad;

  const y = Math.sin(lon2 - lon1) * Math.cos(lat2);
  const x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(lon2 - lon1);
  const theta = Math.atan2(y, x);
  return (theta * 180 / Math.PI + 360) % 360;
}

// -------------------------------------------------------------
// 5. Dijkstra's Algorithm (Min-Heap Priority Queue)
// Solves: Guaranteed shortest-distance pedestrian routing (O((V + E) log V))
// -------------------------------------------------------------
function runDijkstra(graph, startNode, endNode, nodesCoord, options = {}) {
  startNode = String(startNode);
  endNode = String(endNode);
  const t0 = performance.now();
  const { accessibleOnly = false } = options;

  const dist = {};
  const prev = {};
  const visited = new Set();
  const pq = new MinHeap();

  dist[startNode] = 0;
  pq.push({ id: startNode, priority: 0 });

  let nodesVisitedCount = 0;

  while (!pq.isEmpty()) {
    const { id: u, priority: currentDist } = pq.pop();

    if (visited.has(u)) continue;
    visited.add(u);
    nodesVisitedCount++;

    if (u === endNode) break;

    const neighbors = graph[u] || [];
    for (const edge of neighbors) {
      const v = edge.to;

      // Skip non-accessible paths (steps/stairs) if wheelchair/accessibility requested
      if (accessibleOnly && edge.type === 'steps') continue;

      const alt = currentDist + edge.dist;
      if (dist[v] === undefined || alt < dist[v]) {
        dist[v] = alt;
        prev[v] = { node: u, dist: edge.dist, type: edge.type };
        pq.push({ id: v, priority: alt });
      }
    }
  }

  const executionTimeMs = performance.now() - t0;

  if (dist[endNode] === undefined) {
    return {
      success: false,
      algorithm: "Dijkstra's Algorithm",
      path: [],
      distance: 0,
      nodesVisited: nodesVisitedCount,
      executionTimeMs: Math.max(0.01, parseFloat(executionTimeMs.toFixed(3))),
      error: "No connected path found."
    };
  }

  // Reconstruct path
  const path = [];
  let curr = endNode;
  let exactGeometricDistance = 0;

  while (curr !== startNode) {
    path.push(curr);
    const p = prev[curr];
    if (!p) break;
    exactGeometricDistance += p.dist;
    curr = p.node;
  }
  path.push(startNode);
  path.reverse();

  return {
    success: true,
    algorithm: "Dijkstra's Algorithm",
    path,
    distance: Math.round(exactGeometricDistance),
    nodesVisited: nodesVisitedCount,
    executionTimeMs: Math.max(0.01, parseFloat(executionTimeMs.toFixed(3)))
  };
}

// -------------------------------------------------------------
// 6. Breadth-First Search (BFS) - Unweighted Fewest Hops / Intersections
// Solves: Minimum turn & junction navigation; Graph connectivity audit
// -------------------------------------------------------------
function runBFS(graph, startNode, endNode, nodesCoord, options = {}) {
  startNode = String(startNode);
  endNode = String(endNode);
  const t0 = performance.now();
  const { accessibleOnly = false } = options;

  const queue = [startNode];
  const visited = new Set([startNode]);
  const prev = {};
  let nodesVisitedCount = 0;
  let found = false;

  while (queue.length > 0) {
    const u = queue.shift();
    nodesVisitedCount++;

    if (u === endNode) {
      found = true;
      break;
    }

    const neighbors = graph[u] || [];
    for (const edge of neighbors) {
      const v = edge.to;
      if (visited.has(v)) continue;
      if (accessibleOnly && edge.type === 'steps') continue;

      visited.add(v);
      prev[v] = { node: u, dist: edge.dist };
      queue.push(v);
    }
  }

  const executionTimeMs = performance.now() - t0;

  if (!found) {
    return {
      success: false,
      algorithm: "BFS (Breadth-First)",
      path: [],
      distance: 0,
      nodesVisited: nodesVisitedCount,
      executionTimeMs: Math.max(0.01, parseFloat(executionTimeMs.toFixed(3)))
    };
  }

  const path = [];
  let curr = endNode;
  let totalDist = 0;
  while (curr !== startNode) {
    path.push(curr);
    const p = prev[curr];
    if (!p) break;
    totalDist += p.dist;
    curr = p.node;
  }
  path.push(startNode);
  path.reverse();

  return {
    success: true,
    algorithm: "BFS (Breadth-First)",
    path,
    distance: Math.round(totalDist),
    nodesVisited: nodesVisitedCount,
    hops: path.length - 1,
    executionTimeMs: Math.max(0.01, parseFloat(executionTimeMs.toFixed(3)))
  };
}

// -------------------------------------------------------------
// 7. Depth-First Search (DFS) - Deep Path Traversal
// Solves: Path exploration, reachability & comparative benchmark
// -------------------------------------------------------------
function runDFS(graph, startNode, endNode, nodesCoord, options = {}) {
  startNode = String(startNode);
  endNode = String(endNode);
  const t0 = performance.now();
  const { accessibleOnly = false } = options;

  const stack = [startNode];
  const visited = new Set();
  const prev = {};
  let nodesVisitedCount = 0;
  let found = false;

  while (stack.length > 0) {
    const u = stack.pop();
    if (visited.has(u)) continue;
    visited.add(u);
    nodesVisitedCount++;

    if (u === endNode) {
      found = true;
      break;
    }

    const neighbors = graph[u] || [];
    for (const edge of neighbors) {
      const v = edge.to;
      if (visited.has(v)) continue;
      if (accessibleOnly && edge.type === 'steps') continue;

      if (!prev[v]) {
        prev[v] = { node: u, dist: edge.dist };
      }
      stack.push(v);
    }
  }

  const executionTimeMs = performance.now() - t0;

  if (!found) {
    return {
      success: false,
      algorithm: "DFS (Depth-First)",
      path: [],
      distance: 0,
      nodesVisited: nodesVisitedCount,
      executionTimeMs: Math.max(0.01, parseFloat(executionTimeMs.toFixed(3)))
    };
  }

  const path = [];
  let curr = endNode;
  let totalDist = 0;
  while (curr !== startNode) {
    path.push(curr);
    const p = prev[curr];
    if (!p) break;
    totalDist += p.dist;
    curr = p.node;
  }
  path.push(startNode);
  path.reverse();

  return {
    success: true,
    algorithm: "DFS (Depth-First)",
    path,
    distance: Math.round(totalDist),
    nodesVisited: nodesVisitedCount,
    hops: path.length - 1,
    executionTimeMs: Math.max(0.01, parseFloat(executionTimeMs.toFixed(3)))
  };
}

// -------------------------------------------------------------
// 8. Kruskal's Algorithm (Minimum Spanning Tree)
// Solves: Campus Infrastructure Connectivity (fiber-optic / pipeline cabling layout)
// -------------------------------------------------------------
function runKruskalMST(landmarks, graph, nodesCoord) {
  const t0 = performance.now();

  const landmarkNodes = landmarks.map(lm => lm.nearest_node);
  const n = landmarkNodes.length;
  const candidateEdges = [];

  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      const u = landmarkNodes[i];
      const v = landmarkNodes[j];
      const res = runDijkstra(graph, u, v, nodesCoord);
      if (res.success) {
        candidateEdges.push({
          u,
          v,
          dist: res.distance,
          path: res.path,
          sourceName: landmarks[i].name,
          targetName: landmarks[j].name
        });
      }
    }
  }

  // Sort candidate edges ascending by weight
  candidateEdges.sort((a, b) => a.dist - b.dist);

  const dsu = new DSU(landmarkNodes);
  const mstEdges = [];
  let totalMstLength = 0;

  for (const edge of candidateEdges) {
    if (dsu.union(edge.u, edge.v)) {
      mstEdges.push(edge);
      totalMstLength += edge.dist;
      if (mstEdges.length === n - 1) break;
    }
  }

  const executionTimeMs = performance.now() - t0;

  return {
    algorithm: "Kruskal's MST",
    treeEdges: mstEdges,
    totalLengthMeters: Math.round(totalMstLength),
    connectedLandmarksCount: n,
    executionTimeMs: Math.max(0.1, parseFloat(executionTimeMs.toFixed(2)))
  };
}

// -------------------------------------------------------------
// 9. Prim's Algorithm (Minimum Spanning Tree)
// Solves: Vertex-Centric Infrastructure Expansion starting from Admin Block
// -------------------------------------------------------------
function runPrimMST(landmarks, graph, nodesCoord, startLandmarkId = "admin_block") {
  const t0 = performance.now();

  const startLm = landmarks.find(l => l.id === startLandmarkId) || landmarks[0];
  const startNode = startLm.nearest_node;

  const inMST = new Set([startNode]);
  const mstEdges = [];
  let totalLength = 0;

  const pq = new MinHeap();

  function addLandmarkEdges(u) {
    for (const lm of landmarks) {
      const v = lm.nearest_node;
      if (!inMST.has(v)) {
        const res = runDijkstra(graph, u, v, nodesCoord);
        if (res.success) {
          pq.push({
            u,
            v,
            priority: res.distance,
            dist: res.distance,
            path: res.path,
            sourceName: landmarks.find(l => l.nearest_node === u)?.name || "Unknown",
            targetName: lm.name
          });
        }
      }
    }
  }

  addLandmarkEdges(startNode);

  while (!pq.isEmpty() && inMST.size < landmarks.length) {
    const edge = pq.pop();
    if (inMST.has(edge.v)) continue;

    inMST.add(edge.v);
    mstEdges.push(edge);
    totalLength += edge.dist;

    addLandmarkEdges(edge.v);
  }

  const executionTimeMs = performance.now() - t0;

  return {
    algorithm: "Prim's MST",
    treeEdges: mstEdges,
    totalLengthMeters: Math.round(totalLength),
    connectedLandmarksCount: inMST.size,
    executionTimeMs: Math.max(0.1, parseFloat(executionTimeMs.toFixed(2)))
  };
}

// -------------------------------------------------------------
// 10. Dynamic Programming: Task 1 - Weighted Interval Scheduling
// Solves: Non-conflicting Fest & Venue Allocation with Maximum Utility (O(N log N))
// -------------------------------------------------------------
function runDPEventAllocation(events) {
  const sorted = [...events].sort((a, b) => a.end - b.end);
  const n = sorted.length;

  function findLatestNonConflict(i) {
    for (let j = i - 1; j >= 0; j--) {
      if (sorted[j].end <= sorted[i].start) {
        return j;
      }
    }
    return -1;
  }

  const dp = new Array(n).fill(0);
  const selected = new Array(n).fill(null).map(() => []);

  dp[0] = sorted[0].utility;
  selected[0] = [sorted[0]];

  for (let i = 1; i < n; i++) {
    // Option 1: Include event i
    let includeUtility = sorted[i].utility;
    const l = findLatestNonConflict(i);
    let includeList = [sorted[i]];
    if (l !== -1) {
      includeUtility += dp[l];
      includeList = [...selected[l], sorted[i]];
    }

    // Option 2: Exclude event i
    const excludeUtility = dp[i - 1];

    if (includeUtility > excludeUtility) {
      dp[i] = includeUtility;
      selected[i] = includeList;
    } else {
      dp[i] = excludeUtility;
      selected[i] = [...selected[i - 1]];
    }
  }

  return {
    maxUtilityScore: dp[n - 1],
    scheduledEvents: selected[n - 1],
    totalEventsConsidered: n,
    algorithm: "Weighted Interval Scheduling via Dynamic Programming (O(N log N))"
  };
}

// -------------------------------------------------------------
// 11. Dynamic Programming: Task 2 - 0/1 Knapsack Resource Allocation
// Solves: Department Equipment & Budget Capacity Allocation (O(N · W))
// -------------------------------------------------------------
function runDPKnapsack(items, capacity) {
  const n = items.length;
  // dp[i][w] = max utility with subset of first i items within capacity w
  const dp = Array.from({ length: n + 1 }, () => new Array(capacity + 1).fill(0));

  for (let i = 1; i <= n; i++) {
    const { cost, utility } = items[i - 1];
    for (let w = 0; w <= capacity; w++) {
      if (cost <= w) {
        dp[i][w] = Math.max(dp[i - 1][w], dp[i - 1][w - cost] + utility);
      } else {
        dp[i][w] = dp[i - 1][w];
      }
    }
  }

  // Backtrack to find selected items
  const selected = [];
  let w = capacity;
  for (let i = n; i > 0 && w > 0; i--) {
    if (dp[i][w] !== dp[i - 1][w]) {
      selected.push(items[i - 1]);
      w -= items[i - 1].cost;
    }
  }
  selected.reverse();

  const totalCost = selected.reduce((sum, item) => sum + item.cost, 0);

  return {
    algorithm: "0/1 Knapsack via Dynamic Programming (O(N · W))",
    maxUtilityScore: dp[n][capacity],
    totalCost,
    remainingCapacity: capacity - totalCost,
    allocatedItems: selected,
    totalItemsConsidered: n
  };
}

// -------------------------------------------------------------
// 12. Turn-by-Turn Cardinal Directions Generator
// -------------------------------------------------------------
function generateDirections(pathNodeIds, nodesCoord, landmarks) {
  if (!pathNodeIds || pathNodeIds.length < 2) return [];

  const directions = [];
  const coords = pathNodeIds.map(id => nodesCoord[id]);

  const startCoord = coords[0];
  const endCoord = coords[coords.length - 1];

  let initialHeading = calculateBearing(coords[0], coords[1]);
  let cardinal = getCardinal(initialHeading);

  directions.push({
    step: 1,
    action: "start",
    instruction: `Start from departure point heading ${cardinal}.`,
    distance: 0,
    coord: startCoord
  });

  let accumDist = 0;
  let lastBearing = initialHeading;

  for (let i = 1; i < coords.length - 1; i++) {
    const segDist = haversineDistance(coords[i - 1], coords[i]);
    accumDist += segDist;

    const currentBearing = calculateBearing(coords[i], coords[i + 1]);
    let turnAngle = (currentBearing - lastBearing + 540) % 360 - 180;

    const nearbyLm = landmarks.find(lm => {
      const c = lm.coords || [lm.lat, lm.lon];
      return c && c.length === 2 && haversineDistance(coords[i], c) < 30;
    });
    const landmarkHint = nearbyLm ? ` (passing by ${nearbyLm.name})` : "";

    const currNodeId = pathNodeIds[i];
    if (currNodeId === "admin_west_entrance") {
      directions.push({
        step: directions.length + 1,
        action: "corridor",
        instruction: `In ${Math.round(accumDist)} meters, enter Admin Block and cross through the ground-floor corridor.`,
        distance: Math.round(accumDist),
        coord: coords[i]
      });
      accumDist = 0;
      lastBearing = currentBearing;
      continue;
    } else if (currNodeId === "b6_central_lobby") {
      directions.push({
        step: directions.length + 1,
        action: "corridor",
        instruction: `Cross through Block 6 central lobby / hallway (indoor corridor).`,
        distance: Math.round(accumDist),
        coord: coords[i]
      });
      accumDist = 0;
      lastBearing = currentBearing;
      continue;
    } else if (currNodeId === "gate_b5_library") {
      directions.push({
        step: directions.length + 1,
        action: "gate",
        instruction: `In ${Math.round(accumDist)} meters, pass through the gate between Block 5 and the Library toward TnP.`,
        distance: Math.round(accumDist),
        coord: coords[i]
      });
      accumDist = 0;
      lastBearing = currentBearing;
      continue;
    }

    if (Math.abs(turnAngle) >= 35 && accumDist >= 20) {
      let turnAction = "slight right";
      if (turnAngle < -45) turnAction = "sharp left";
      else if (turnAngle < -25) turnAction = "left";
      else if (turnAngle > 45) turnAction = "sharp right";
      else if (turnAngle > 25) turnAction = "right";

      directions.push({
        step: directions.length + 1,
        action: turnAction.includes("left") ? "turn-left" : "turn-right",
        instruction: `In ${Math.round(accumDist)} meters, turn ${turnAction}${landmarkHint}.`,
        distance: Math.round(accumDist),
        coord: coords[i]
      });

      accumDist = 0;
      lastBearing = currentBearing;
    }
  }

  const finalSegDist = haversineDistance(coords[coords.length - 2], coords[coords.length - 1]);
  accumDist += finalSegDist;

  directions.push({
    step: directions.length + 1,
    action: "destination",
    instruction: `Walk ${Math.round(accumDist)} meters to arrive at your destination.`,
    distance: Math.round(accumDist),
    coord: endCoord
  });

  return directions;
}

function getCardinal(angle) {
  const directions = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"];
  const index = Math.round(angle / 45) % 8;
  return directions[index];
}

// Global Export
window.CampusAlgorithms = {
  MinHeap,
  DSU,
  CampusHashTable,
  AVLTree,
  AVLNode,
  haversineDistance,
  calculateBearing,
  runDijkstra,
  runBFS,
  runDFS,
  runKruskalMST,
  runPrimMST,
  runDPEventAllocation,
  runDPKnapsack,
  generateDirections,
  generateTurnByTurn: generateDirections
};
