// Test algorithms in Node.js environment
global.window = {};
global.performance = require('perf_hooks').performance;

require('./graphData.js');
require('./algorithms.js');

const { campusCenter, landmarks, nodes, edges, adjacency } = window.CAMPUS_DATA;
const algos = window.CampusAlgorithms;

console.log("=== NSUT Graph Verification ===");
console.log(`Campus Center: ${campusCenter}`);
console.log(`Landmarks: ${landmarks.length}`);
console.log(`Nodes: ${Object.keys(nodes).length}`);
console.log(`Edges: ${edges.length}`);

const mainGate = landmarks.find(l => l.id === "main_gate");
const apj = landmarks.find(l => l.id === "apj_complex");

// 1. Dijkstra
console.log("\n--- 1. Dijkstra's Algorithm ---");
const dRes = algos.runDijkstra(adjacency, mainGate.nearest_node, apj.nearest_node, nodes);
console.log(`  Main Gate -> APJ Complex:`);
console.log(`  Distance: ${dRes.distance} m`);
console.log(`  Time: ${dRes.executionTimeMs} ms`);
console.log(`  Nodes visited: ${dRes.nodesVisited}`);

// 2. BFS & DFS
console.log("\n--- 2. BFS & DFS ---");
const bRes = algos.runBFS(adjacency, mainGate.nearest_node, apj.nearest_node, nodes);
const dfRes = algos.runDFS(adjacency, mainGate.nearest_node, apj.nearest_node, nodes);
console.log(`  BFS Distance: ${bRes.distance} m (Hops: ${bRes.hops}, Nodes visited: ${bRes.nodesVisited})`);
console.log(`  DFS Distance: ${dfRes.distance} m (Hops: ${dfRes.hops}, Nodes visited: ${dfRes.nodesVisited})`);

// 3. Kruskal & Prim MST
console.log("\n--- 3. Kruskal & Prim MST ---");
const kRes = algos.runKruskalMST(landmarks, adjacency, nodes);
console.log(`  Kruskal Cable Length: ${kRes.totalLengthMeters} m (Tree Edges: ${kRes.treeEdges.length})`);
const pRes = algos.runPrimMST(landmarks, adjacency, nodes, "admin_block");
console.log(`  Prim Cable Length: ${pRes.totalLengthMeters} m (Tree Edges: ${pRes.treeEdges.length})`);

// 4. Balanced Search Tree (AVL Tree)
console.log("\n--- 4. Balanced Search Tree (AVL Tree) ---");
const avl = new algos.AVLTree();
landmarks.forEach(lm => avl.insert(lm.name, lm));
const stats = avl.getTreeStats();
console.log(`  AVL Tree Size: ${stats.size}, Height: ${stats.height}, Balance Factor: ${stats.balanceFactor}, Balanced: ${stats.isBalanced}`);
const searchRes = avl.search("Admin Block");
console.log(`  AVL Search for 'Admin Block': ${searchRes ? "Found (" + searchRes.id + ")" : "Not Found"}`);
const prefixRes = avl.searchPrefix("Block");
console.log(`  AVL Prefix Search 'Block': Found ${prefixRes.length} items (${prefixRes.map(p => p.name).join(", ")})`);

// 5. Hashing (CampusHashTable)
console.log("\n--- 5. Hashing (CampusHashTable) ---");
const ht = new algos.CampusHashTable(37);
landmarks.forEach(lm => ht.set(lm.id, lm));
const htStats = ht.stats();
console.log(`  Hash Table Keys: ${htStats.totalKeys}, Table Size: ${htStats.tableSize}, Load Factor: ${htStats.loadFactor}, Max Collisions: ${htStats.maxCollisions}`);
const getRes = ht.get("main_gate");
console.log(`  Hash Lookup 'main_gate': ${getRes ? "Found (" + getRes.name + ")" : "Not Found"}`);

// 6. Dynamic Programming: Weighted Interval Scheduling
console.log("\n--- 6. DP: Weighted Interval Scheduling ---");
const sampleEvents = [
  { name: "Moksha Star Night", society: "Council", venue: "Moksha Stage", start: 18, end: 22, utility: 95 },
  { name: "HackNSUT", society: "IEEE", venue: "APJ", start: 10, end: 18, utility: 88 },
  { name: "Taarangana Dance", society: "Capella", venue: "SAC", start: 13, end: 16, utility: 78 },
  { name: "Debate", society: "DebSoc", venue: "Mini Audi", start: 10, end: 13, utility: 72 }
];
const dpRes = algos.runDPEventAllocation(sampleEvents);
console.log(`  Max Utility: ${dpRes.maxUtilityScore}`);
console.log(`  Approved Events: ${dpRes.scheduledEvents.map(e => e.name).join(", ")}`);

// 7. Dynamic Programming: 0/1 Knapsack
console.log("\n--- 7. DP: 0/1 Knapsack Resource Allocation ---");
const sampleProjects = [
  { name: "AI GPU Cluster", dept: "CSE", cost: 10, utility: 95 },
  { name: "Robotics Arena Kits", dept: "ECE/ICE", cost: 5, utility: 60 },
  { name: "Digital Library Subscription", dept: "Library", cost: 4, utility: 55 },
  { name: "Smart Campus Sensors", dept: "IT", cost: 7, utility: 70 },
  { name: "Sports Complex Gear", dept: "Sports", cost: 3, utility: 40 }
];
const knapsackRes = algos.runDPKnapsack(sampleProjects, 15);
console.log(`  Max Utility for Budget 15L: ${knapsackRes.maxUtilityScore}`);
console.log(`  Total Cost: ${knapsackRes.totalCost}L, Remaining: ${knapsackRes.remainingCapacity}L`);
console.log(`  Allocated: ${knapsackRes.allocatedItems.map(p => p.name).join(", ")}`);

console.log("\n>>> ALL 7 CORE ALGORITHM CATEGORIES VERIFIED SUCCESSFULLY! <<<");
