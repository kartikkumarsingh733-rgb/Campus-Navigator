import json
import heapq

with open("landmarks_snapped.json", "r", encoding="utf-8") as f:
    landmarks = json.load(f)

with open("build_graph.py", "r", encoding="utf-8") as f:
    pass

import build_graph
graph = build_graph.graph
nodes = build_graph.nodes

def dijkstra(start_node, target_node):
    dist = {start_node: 0.0}
    prev = {}
    pq = [(0.0, start_node)]
    visited = set()
    
    while pq:
        d, u = heapq.heappop(pq)
        if u in visited: continue
        visited.add(u)
        
        if u == target_node:
            break
            
        for edge in graph.get(u, []):
            v = edge["to"]
            weight = edge["dist"]
            if dist.get(v, float('inf')) > d + weight:
                dist[v] = d + weight
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
                
    if target_node not in dist:
        return None, float('inf')
        
    path = []
    curr = target_node
    while curr in prev:
        path.append(curr)
        curr = prev[curr]
    path.append(start_node)
    path.reverse()
    return path, dist[target_node]

lm_by_id = {lm["id"]: lm for lm in landmarks}

test_pairs = [
    ("main_gate", "apj_complex"),
    ("north_gate", "central_library"),
    ("boys_hostels", "student_center"),
    ("admin_block", "sports_grounds"),
    ("kaveri_hostel", "sac"),
    ("amul_ground", "block_6")
]

print("Testing Dijkstra routing between campus landmarks:")
for src_id, dst_id in test_pairs:
    src = lm_by_id[src_id]
    dst = lm_by_id[dst_id]
    path, total_dist = dijkstra(src["nearest_node"], dst["nearest_node"])
    if path:
        walking_time_mins = (total_dist / 80)  # average walking speed ~80 m/min (4.8 km/h)
        print(f"  {src['name']} -> {dst['name']}: {total_dist:.1f} m (~{walking_time_mins:.1f} mins, {len(path)} waypoints)")
    else:
        print(f"  FAILED: {src['name']} -> {dst['name']}")

