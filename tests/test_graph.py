from app.graph import build_adjacency_list, find_all_paths, find_cheapest_path

EDGES = [
    {"from": "a", "to": "b", "cost": 1.0},
    {"from": "b", "to": "e", "cost": 2.0},
    {"from": "a", "to": "c", "cost": 5.0},
    {"from": "c", "to": "e", "cost": 1.0},
    {"from": "a", "to": "e", "cost": 10.0},
]

def test_build_adjacency_list():
    adjacency = build_adjacency_list(EDGES)
    assert "a" in adjacency
    assert "e" not in adjacency  # e has no outgoing edges
    assert len(adjacency["a"]) == 3

def test_find_all_paths():
    adjacency = build_adjacency_list(EDGES)
    paths = find_all_paths(adjacency, "a", "e")
    assert len(paths) == 3
    assert ["a", "e"] in paths
    assert ["a", "b", "e"] in paths
    assert ["a", "c", "e"] in paths

def test_find_all_paths_no_path():
    adjacency = build_adjacency_list(EDGES)
    paths = find_all_paths(adjacency, "a", "d")
    assert paths == []

def test_cheapest_path():
    adjacency = build_adjacency_list(EDGES)
    path = find_cheapest_path(adjacency, "a", "e")
    assert path == ["a", "b", "e"]

def test_cheapest_path_no_path():
    adjacency = build_adjacency_list(EDGES)
    path = find_cheapest_path(adjacency, "a", "d")
    assert path is None

def test_cheapest_path_direct():
    # Test that direct path is chosen when it's cheapest
    edges = [
        {"from": "a", "to": "b", "cost": 1.0},
        {"from": "a", "to": "b", "cost": 100.0},
    ]
    adjacency = build_adjacency_list(edges)
    path = find_cheapest_path(adjacency, "a", "b")
    assert path == ["a", "b"]