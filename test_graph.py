from app.graph import build_adjacency_list, find_all_paths, find_cheapest_path

edges = [
    {"from": "a", "to": "b", "cost": 1.0},
    {"from": "b", "to": "e", "cost": 2.0},
    {"from": "a", "to": "c", "cost": 5.0},
    {"from": "c", "to": "e", "cost": 1.0},
    {"from": "a", "to": "e", "cost": 10.0},
]

adjacency = build_adjacency_list(edges)
print("Adjacency list:", adjacency)

# Should return 3 paths
paths = find_all_paths(adjacency, "a", "e")
print("\nAll paths a->e:", paths)

# Should return ["a", "b", "e"] with cost 3.0
cheapest = find_cheapest_path(adjacency, "a", "e")
print("\nCheapest path a->e:", cheapest)

# Should return None (no path exists)
no_path = find_cheapest_path(adjacency, "a", "d")
print("\nCheapest path a->d:", no_path)