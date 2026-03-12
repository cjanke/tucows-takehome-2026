-- Nodes and edges representing sample/sample_graph.xml
-- Insert graph
INSERT INTO graphs (id, name) VALUES ('g0', 'The Graph Name');

-- Insert nodes
INSERT INTO nodes (id, graph_id, name) VALUES
    ('a', 'g0', 'A name'),
    ('b', 'g0', 'B name'),
    ('c', 'g0', 'C name'),
    ('d', 'g0', 'D name'),
    ('e', 'g0', 'E name');

-- Insert edges
INSERT INTO edges (id, graph_id, from_node, to_node, cost) VALUES
    ('e1', 'g0', 'a', 'b', 1.0),
    ('e2', 'g0', 'b', 'e', 2.0),
    ('e3', 'g0', 'a', 'c', 5.0),
    ('e4', 'g0', 'c', 'e', 1.0),
    ('e5', 'g0', 'a', 'e', 10.0),
    ('e6', 'g0', 'd', 'e', 1.0),
    ('e7', 'g0', 'a', 'a', 0.0);

-- CYCLE DETECTION SQL
-- Uncomment the below lines to test cycle detection
-- INSERT INTO edges (id, graph_id, from_node, to_node, cost)
-- VALUES ('e8', 'g0', 'e', 'a', 1.0);