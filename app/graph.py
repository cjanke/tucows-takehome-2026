import heapq

def build_adjacency_list(edges: list[dict]) -> dict[str, list[tuple[str, float]]]:
    """
    Build an adjacency list from a list of edge dicts.
    Returns a dict mapping each node to a list of (neighbour, cost) tuples.
    """
    adjacency = {}
    for edge in edges:
        from_node = edge["from"]
        to_node = edge["to"]
        cost = edge["cost"]
        if from_node not in adjacency:
            adjacency[from_node] = []
        adjacency[from_node].append((to_node, cost))
    return adjacency

def find_all_paths(
    adjacency: dict[str, list[tuple[str, float]]],
    start: str,
    end: str,
    visited: set[str] | None = None,
    current_path: list[str] | None = None
) -> list[list[str]]:
    """
    Find all paths from start to end using DFS.
    Returns a list of paths, where each path is a list of node IDs.
    """
    if visited is None:
        visited = set()
    if current_path is None:
        current_path = []

    visited.add(start)
    current_path.append(start)

    paths = []

    if start == end:
        paths.append(current_path.copy())
    else:
        for neighbor, _ in adjacency.get(start, []):
            if neighbor not in visited:
                new_paths = find_all_paths(adjacency, neighbor, end, visited, current_path)
                paths.extend(new_paths)

    # Backtrack
    current_path.pop()
    visited.remove(start)

    return paths

def find_cheapest_path(
    adjacency: dict[str, list[tuple[str, float]]],
    start: str,
    end: str
) -> list[str] | None:
    """
    Find the cheapest path from start to end using Dijkstra's algorithm.
    Returns a list of node IDs, or None if no path exists.
    """
    # Each entry in the heap is (cost, node, path)
    heap = [(0.0, start, [start])]
    visited = set()

    while heap:
        cost, node, path = heapq.heappop(heap)

        if node in visited:
            continue
        visited.add(node)

        if node == end:
            return path

        for neighbour, edge_cost in adjacency.get(node, []):
            if neighbour not in visited:
                heapq.heappush(heap, (cost + edge_cost, neighbour, path + [neighbour]))

    return None