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

def test_missing_file():
    with pytest.raises(GraphParseError, match="File not found"):
        parse_graph("sample/nonexistent.xml")

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