from app.parser import parse_graph, GraphParseError

# Test simple graph
print("Testing simple graph...")
result = parse_graph("sample/small_graph.xml")
print(result)

# Test no edges graph
print("\nTesting no edges graph...")
result = parse_graph("sample/no_edges.xml")
print(result)

# Test full graph
print("\nTesting full graph...")
result = parse_graph("sample/sample_graph.xml")
print(result)

# Test error case - bad file path
print("\nTesting bad filepath...")
try:
    parse_graph("sample/nonexistent.xml")
except GraphParseError as e:
    print(f"Caught expected error: {e}")