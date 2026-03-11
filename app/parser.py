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

# We assume one graph per XML file, as the spec defines <graph> as the root element.
# Multiple graphs would require a wrapper element like <graphs> which is not in the spec.
def parse_graph(filepath):
    """
    Parse and validate a graph XML file.
    Returns a dict with keys: id, name, nodes, edges
    Raises GraphParseError if the file is invalid.
    """
    try:
        tree = ET.parse(filepath)
    # only check for specific errors so we don't swallow exceptions
    except ET.ParseError as e:
        raise GraphParseError(f"XML syntax error: {e}")
    except FileNotFoundError:
      raise GraphParseError(f"File not found: {filepath}")

    root = tree.getroot()

    # Validate and extract graph metadata
    graph_id = _require(root, "id", "<graph>")
    graph_name = _require(root, "name", "<graph>")

    # Parse nodes
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

    # Parse edges
    edges = []
    edges_el = root.find("edges")
    if edges_el is not None:
        for edge_el in edges_el.findall("node"):
            edge_id = _require(edge_el, "id", "<edge>")
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

    return {
        "id": graph_id,
        "name": graph_name,
        "nodes": list(nodes.values()),
        "edges": edges
    }