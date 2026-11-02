// NSUT Dwarka Smart Campus Navigation & Resource Optimizer
// Core Data Structures & Graph Algorithms for Viva / End-Sem Project

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
      this.parent[i] = this.find(this.parent[i]); // Path compression
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
// 3. Dijkstra's Algorithm (Min-Heap Priority Queue)
// -------------------------------------------------------------
function runDijkstra(graph, startNode, endNode, nodesCoord, options = {}) {
  startNode = String(startNode);
  endNode = String(endNode);
  const t0 = performance.now();
  const { blockedEdges = new Set(), accessibleOnly = false, weatherFactor = 1.0, rushEdges = new Set() } = options;

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
      const edgeId = edge.edgeId;

      // Skip blocked pathways (e.g. simulated construction)
      if (blockedEdges.has(edgeId)) continue;

      // Skip non-accessible paths (steps/stairs) if wheelchair/accessibility requested
      if (accessibleOnly && edge.type === 'steps') continue;

      // Weight multiplier (weather / congestion)
      let weight = edge.dist;
      if (edge.type === 'path' || edge.type === 'track') {
        weight *= weatherFactor; // Unpaved paths penalty during rain
      }
      if (rushEdges.has(edgeId)) {
        weight *= 1.8; // Peak rush congestion penalty
      }

      const alt = currentDist + weight;
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
      error: "No connected path found (pathway may be blocked or stairs avoided)."
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
    weightedDistance: Math.round(dist[endNode]),
    nodesVisited: nodesVisitedCount,
    executionTimeMs: Math.max(0.01, parseFloat(executionTimeMs.toFixed(3)))
  };
}

// -------------------------------------------------------------
// 4. A* Search Algorithm (Haversine Heuristic)
// -------------------------------------------------------------
function runAStar(graph, startNode, endNode, nodesCoord, options = {}) {
  startNode = String(startNode);
  endNode = String(endNode);
  const t0 = performance.now();
  const { blockedEdges = new Set(), accessibleOnly = false, weatherFactor = 1.0, rushEdges = new Set() } = options;

  const targetCoord = nodesCoord[endNode];
  if (!targetCoord) return { success: false, error: "Target node coordinates missing" };

  const gScore = {};
  const fScore = {};
  const prev = {};
  const visited = new Set();
  const pq = new MinHeap();

  gScore[startNode] = 0;
  const initialH = haversineDistance(nodesCoord[startNode], targetCoord);
  fScore[startNode] = initialH;
  pq.push({ id: startNode, priority: initialH });

  let nodesVisitedCount = 0;

  while (!pq.isEmpty()) {
    const { id: u } = pq.pop();

    if (visited.has(u)) continue;
    visited.add(u);
    nodesVisitedCount++;

    if (u === endNode) break;

    const neighbors = graph[u] || [];
    for (const edge of neighbors) {
      const v = edge.to;
      const edgeId = edge.edgeId;

      if (blockedEdges.has(edgeId)) continue;
      if (accessibleOnly && edge.type === 'steps') continue;

      let weight = edge.dist;
      if (edge.type === 'path' || edge.type === 'track') weight *= weatherFactor;
      if (rushEdges.has(edgeId)) weight *= 1.8;

      const tentativeG = gScore[u] + weight;
      if (gScore[v] === undefined || tentativeG < gScore[v]) {
        prev[v] = { node: u, dist: edge.dist };
        gScore[v] = tentativeG;
        const h = haversineDistance(nodesCoord[v], targetCoord);
        fScore[v] = tentativeG + h;
        pq.push({ id: v, priority: fScore[v] });
      }
    }
  }

  const executionTimeMs = performance.now() - t0;

  if (gScore[endNode] === undefined) {
    return {
      success: false,
      algorithm: "A* Search",
      path: [],
      distance: 0,
      nodesVisited: nodesVisitedCount,
      executionTimeMs: Math.max(0.01, parseFloat(executionTimeMs.toFixed(3))),
      error: "No path found"
    };
  }

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
    algorithm: "A* Search",
    path,
    distance: Math.round(exactGeometricDistance),
    weightedDistance: Math.round(gScore[endNode]),
    nodesVisited: nodesVisitedCount,
    executionTimeMs: Math.max(0.01, parseFloat(executionTimeMs.toFixed(3)))
  };
}

// -------------------------------------------------------------
// 5. Breadth-First Search (BFS) - Unweighted Shortest Hops
// -------------------------------------------------------------
function runBFS(graph, startNode, endNode, nodesCoord, options = {}) {
  startNode = String(startNode);
  endNode = String(endNode);
  const t0 = performance.now();
  const { blockedEdges = new Set(), accessibleOnly = false } = options;

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
      if (blockedEdges.has(edge.edgeId)) continue;
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
// 6. Depth-First Search (DFS) - Path Exploration
// -------------------------------------------------------------
function runDFS(graph, startNode, endNode, nodesCoord, options = {}) {
  startNode = String(startNode);
  endNode = String(endNode);
  const t0 = performance.now();
  const { blockedEdges = new Set(), accessibleOnly = false } = options;

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
      if (blockedEdges.has(edge.edgeId)) continue;
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
// 7. Kruskal's Algorithm (Minimum Spanning Tree - Campus Connectivity)
// Solves: Minimum fiber-optic cable / pipeline layout connecting campus landmarks
// -------------------------------------------------------------
function runKruskalMST(landmarks, graph, nodesCoord) {
  const t0 = performance.now();

  // Create an overlay complete graph between all 27 landmark nodes
  // using Dijkstra shortest path distances as edge weights
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
// 8. Prim's Algorithm (Minimum Spanning Tree)
// Starts from Admin Block and greedily expands
// -------------------------------------------------------------
function runPrimMST(landmarks, graph, nodesCoord, startLandmarkId = "admin_block") {
  const t0 = performance.now();

  const landmarkNodes = landmarks.map(lm => lm.nearest_node);
  const startLm = landmarks.find(l => l.id === startLandmarkId) || landmarks[0];
  const startNode = startLm.nearest_node;

  const inMST = new Set([startNode]);
  const mstEdges = [];
  let totalLength = 0;

  // Min-Heap of available edges to non-MST landmarks
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
// 9. Resource / Event Allocation Optimizer (Dynamic Programming)
// Syllabus: "dynamic programming for selected resource-allocation tasks"
// Problem: Given campus venues (Admin Audi, APJ Halls, Moksha Stage, SAC)
// and multiple college fest events with [startTime, endTime, expectedAttendance, utilityScore],
// select the optimal subset of non-overlapping events to maximize total utility/impact!
// -------------------------------------------------------------
function runDPEventAllocation(events, timeSlotLimit = 12) {
  // Sort events by finish time
  const sorted = [...events].sort((a, b) => a.end - b.end);
  const n = sorted.length;

  // Find latest non-conflicting event index for each event (binary search or scan)
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
// 10. Generate Turn-by-Turn Navigation Directions
// -------------------------------------------------------------
function generateDirections(pathNodeIds, nodesCoord, landmarks) {
  if (!pathNodeIds || pathNodeIds.length < 2) return [];

  const directions = [];
  const coords = pathNodeIds.map(id => nodesCoord[id]);

  // Find start and end landmark names
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

    // Check if near any landmark
    const nearbyLm = landmarks.find(lm => {
      const c = lm.coords || [lm.lat, lm.lon];
      return c && c.length === 2 && haversineDistance(coords[i], c) < 30;
    });
    const landmarkHint = nearbyLm ? ` (passing by ${nearbyLm.name})` : "";

    // Check for special indoor breezeways & campus gates
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

// Export functions to window
window.CampusAlgorithms = {
  MinHeap,
  DSU,
  haversineDistance,
  runDijkstra,
  runAStar,
  runBFS,
  runDFS,
  runKruskalMST,
  runPrimMST,
  runDPEventAllocation,
  generateDirections
};

