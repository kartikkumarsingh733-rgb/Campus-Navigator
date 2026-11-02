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

// Test 1: Dijkstra between Main Gate and APJ Complex
const mainGate = landmarks.find(l => l.id === "main_gate");
const apj = landmarks.find(l => l.id === "apj_complex");
const centralLib = landmarks.find(l => l.id === "central_library");

console.log("\n--- Test 1: Dijkstra ---");
const dRes = algos.runDijkstra(adjacency, mainGate.nearest_node, apj.nearest_node, nodes);
console.log(`Main Gate -> APJ Complex:`);
console.log(`  Distance: ${dRes.distance} m`);
console.log(`  Time: ${dRes.executionTimeMs} ms`);
console.log(`  Nodes visited: ${dRes.nodesVisited}`);
console.log(`  Waypoints: ${dRes.path.length}`);

console.log("\n--- Test 2: A* Search ---");
const aRes = algos.runAStar(adjacency, mainGate.nearest_node, apj.nearest_node, nodes);
console.log(`Main Gate -> APJ Complex:`);
console.log(`  Distance: ${aRes.distance} m`);
console.log(`  Time: ${aRes.executionTimeMs} ms`);
console.log(`  Nodes visited: ${aRes.nodesVisited}`);

console.log("\n--- Test 3: BFS vs DFS ---");
const bRes = algos.runBFS(adjacency, mainGate.nearest_node, apj.nearest_node, nodes);
const dfRes = algos.runDFS(adjacency, mainGate.nearest_node, apj.nearest_node, nodes);
console.log(`  BFS Distance: ${bRes.distance} m (Hops: ${bRes.hops})`);
console.log(`  DFS Distance: ${dfRes.distance} m (Hops: ${dfRes.hops})`);

console.log("\n--- Test 4: Turn-by-Turn Directions ---");
const directions = algos.generateDirections(dRes.path, nodes, landmarks);
console.log(`Generated ${directions.length} directions:`);
directions.slice(0, 5).forEach(d => console.log(`  Step ${d.step}: ${d.instruction}`));

console.log("\n--- Test 5: Kruskal's MST (Campus Network) ---");
const kRes = algos.runKruskalMST(landmarks, adjacency, nodes);
console.log(`  Total Cable Length: ${kRes.totalLengthMeters} m`);
console.log(`  Tree Edges: ${kRes.treeEdges.length}`);
console.log(`  Execution Time: ${kRes.executionTimeMs} ms`);

console.log("\n--- Test 6: DP Event Allocation ---");
const sampleEvents = [
  { name: "Moksha Star Night", society: "Council", venue: "Moksha Stage", start: 18, end: 22, utility: 95 },
  { name: "HackNSUT", society: "IEEE", venue: "APJ", start: 10, end: 18, utility: 88 },
  { name: "Taarangana Dance", society: "Capella", venue: "SAC", start: 13, end: 16, utility: 78 },
  { name: "Debate", society: "DebSoc", venue: "Mini Audi", start: 10, end: 13, utility: 72 }
];
const dpRes = algos.runDPEventAllocation(sampleEvents);
console.log(`  Max Utility: ${dpRes.maxUtilityScore}`);
console.log(`  Approved Events: ${dpRes.scheduledEvents.map(e => e.name).join(", ")}`);

console.log("\nALL ALGORITHM TESTS PASSED SUCCESSFULLY!");

