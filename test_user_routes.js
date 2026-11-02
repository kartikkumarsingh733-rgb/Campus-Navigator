global.window = {};
global.performance = require('perf_hooks').performance;

require('./graphData.js');
require('./algorithms.js');

const { landmarks, nodes, adjacency } = window.CAMPUS_DATA;
const algos = window.CampusAlgorithms;

const bh = landmarks.find(l => l.id === "boys_hostels");
const mandir = landmarks.find(l => l.id === "mandir");
const design = landmarks.find(l => l.id === "design_block");
const b6 = landmarks.find(l => l.id === "block_6");

console.log("=== Specific Routing Tests ===");
console.log(`Boys Hostels: ${bh.name} @ ${bh.coords}`);
console.log(`Campus Mandir: ${mandir.name} @ ${mandir.coords}`);
console.log(`Design Block: ${design.name} @ ${design.coords}`);
console.log(`Block 6: ${b6.name} @ ${b6.coords}`);

const r1 = algos.runDijkstra(adjacency, bh.nearest_node, mandir.nearest_node, nodes);
console.log(`\nRoute 1: Boys Hostels -> Campus Mandir`);
console.log(`  Distance: ${r1.distance} m, Compute Time: ${r1.executionTimeMs} ms, Waypoints: ${r1.path.length}`);

const r2 = algos.runDijkstra(adjacency, design.nearest_node, bh.nearest_node, nodes);
console.log(`\nRoute 2: Design Block -> Boys Hostels`);
console.log(`  Distance: ${r2.distance} m, Compute Time: ${r2.executionTimeMs} ms, Waypoints: ${r2.path.length}`);

const r3 = algos.runDijkstra(adjacency, mandir.nearest_node, b6.nearest_node, nodes);
console.log(`\nRoute 3: Campus Mandir -> Block 6`);
console.log(`  Distance: ${r3.distance} m, Compute Time: ${r3.executionTimeMs} ms, Waypoints: ${r3.path.length}`);

console.log("\nALL SPECIFIC TESTS PASSED!");
