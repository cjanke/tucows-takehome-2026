import pytest
from app.parser import parse_graph, GraphParseError

def test_simple_graph():
    result = parse_graph("sample/simple_graph.xml")
    assert result["id"] == "g1"
    assert result["name"] == "Simple Graph"
    assert len(result["nodes"]) == 2
    assert len(result["edges"]) == 1

def test_full_graph():
    result = parse_graph("sample/sample_graph.xml")
    assert result["id"] == "g0"
    assert len(result["nodes"]) == 5
    assert len(result["edges"]) == 7

def test_edge_default_cost():
    result = parse_graph("sample/sample_graph.xml")
    # e7 has no cost in the XML, should default to 0.0
    e7 = next(e for e in result["edges"] if e["id"] == "e7")
    assert e7["cost"] == 0.0

def test_empty_edges():
    result = parse_graph("sample/no_edge_graph.xml")
    assert result["edges"] == []

def test_empty_edges_with_no_edge_tag():
    result = parse_graph("sample/no_edge_graph2.xml")
    assert result["edges"] == []

def test_missing_file():
    with pytest.raises(GraphParseError, match="File not found"):
        parse_graph("sample/nonexistent.xml")

def test_missing_graph_id():
    with pytest.raises(GraphParseError, match="Missing <id> in <graph>"):
      parse_graph("sample/invalid_missing_graph_id_graph.xml")

def test_duplicate_node_ids():
    with pytest.raises(GraphParseError, match="Duplicate node id: 'a'"):
      parse_graph("sample/invalid_duplicate_node_ids_graph.xml")

def test_missing_nodes():
    with pytest.raises(GraphParseError, match="No <nodes> found in graph"):
      parse_graph("sample/invalid_empty_nodes_graph.xml")

def test_edge_must_reference_nodes():
    with pytest.raises(GraphParseError, match="Edge 'e1' references unknown node 'c'"):
      parse_graph("sample/invalid_bad_edge_graph.xml")

def test_edge_only_single_to_node():
    with pytest.raises(GraphParseError, match="Edge 'e1' has 2 <to> tags"):
      parse_graph("sample/invalid_multiple_tos_graph.xml")

def test_invalid_edge_cost():
    with pytest.raises(GraphParseError, match="Edge 'e1' has invalid cost: 'abc'"):
      parse_graph("sample/invalid_edge_cost_graph.xml")

def test_negative_edge_cost():
    with pytest.raises(GraphParseError, match="Edge 'e1' has negative cost"):
      parse_graph("sample/negative_edge_cost_graph.xml")