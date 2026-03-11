import xml.etree.ElementTree as ET

class GraphParseError(Exception):
    """Raised when the XML fails validation."""
    pass

def _require(element, tag, context):
    """Helper to extract a required text field, raising an error if missing."""
    child = element.find(tag)
    if child is None or not child.text:
        raise GraphParseError(f"Missing <{tag}> in {context}")
    return child.text.strip()

def parse_graph(filepath: str):
    """
    Parse and validate a graph XML file.
    Returns a dict with keys: id, name, nodes, edges
    Raises GraphParseError if the file is invalid or not found.
    """
    try:
        tree = ET.parse(filepath)
    except ET.ParseError as e:
        raise GraphParseError(f"XML syntax error: {e}")
    except FileNotFoundError:
        raise GraphParseError(f"File not found: {filepath}")

    root = tree.getroot()

    # We assume one graph per XML file, as the spec defines <graph> as the root element.
    # Multiple graphs would require a wrapper element like <graphs> which is not in the spec.
    graph_id = _require(root, "id", "<graph>")
    graph_name = _require(root, "name", "<graph>")

    nodes = _parse_nodes(root)
    edges = _parse_edges(root, nodes)

    return {"id": graph_id, "name": graph_name, "nodes": list(nodes.values()), "edges": edges}

def _parse_nodes(root: ET.Element) -> dict[str, dict[str, str]]:
    """
    Parse and validate graph nodes from ET root element.
    Returns a dictionary of mappings from node_id => {node_id, node_name}
    Raises GraphParseError if there are any duplicate node ids
    """
    nodes_el = root.find("nodes")
    if nodes_el is None or len(nodes_el) == 0:
        raise GraphParseError("No <nodes> found in graph")

    nodes = {}
    for node_el in nodes_el.findall("node"):
        node_id = _require(node_el, "id", "<node>")
        node_name = _require(node_el, "name", "<node>")

        if node_id in nodes:
            raise GraphParseError(f"Duplicate node id: '{node_id}'")

        nodes[node_id] = {"id": node_id, "name": node_name}

    return nodes

def _parse_edges(root: ET.Element, nodes: dict[str, dict[str, str]]) -> list[dict[str, str | float]]:
    """
    Parse and validate graph edges from ET root element.
    Returns a list of edges, with each edge represented as a dict with keys: id, from, to, cost
    Raises GraphParseError if:
      - A node in an edge does not exist
      - If edge has a negative or invalid cost
    """
    edges = []
    edges_el = root.find("edges")

    if edges_el is None or len(edges_el) == 0:
        return edges

    for edge_el in edges_el.findall("node"):
        edge_id = _require(edge_el, "id", "<edge>")

        num_from_tags = len(edge_el.findall("from"))
        num_to_tags = len(edge_el.findall("to"))
        if num_from_tags != 1:
            raise GraphParseError(f"Edge '{edge_id}' has {num_from_tags} <from> tags")
        if num_to_tags != 1:
            raise GraphParseError(f"Edge '{edge_id}' has {num_to_tags} <to> tags")

        from_node = _require(edge_el, "from", f"<edge id='{edge_id}'>")
        to_node = _require(edge_el, "to", f"<edge id='{edge_id}'>")

        # Validate that from_node and to_node reference existing nodes
        if from_node not in nodes:
            raise GraphParseError(f"Edge '{edge_id}' references unknown node '{from_node}'")
        if to_node not in nodes:
            raise GraphParseError(f"Edge '{edge_id}' references unknown node '{to_node}'")

        # Cost is optional, defaults to 0
        cost_el = edge_el.find("cost")
        if cost_el is not None:
            try:
                cost = float(cost_el.text.strip())
                if cost < 0:
                    raise GraphParseError(f"Edge '{edge_id}' has negative cost")
            except ValueError:
                raise GraphParseError(f"Edge '{edge_id}' has invalid cost: '{cost_el.text}'")
        else:
            cost = 0.0

        edges.append({
            "id": edge_id,
            "from": from_node,
            "to": to_node,
            "cost": cost
        })

    return edges