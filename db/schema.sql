-- Stores the top-level graph metadata
CREATE TABLE graphs (
    id   TEXT PRIMARY KEY,  -- from <id> in XML e.g. "g0"
    name TEXT NOT NULL      -- from <name> in XML e.g. "The Graph Name"
);

-- Stores individual nodes, each belonging to a graph
CREATE TABLE nodes (
    id       TEXT NOT NULL,           -- from <id> in XML e.g. "a"
    graph_id TEXT NOT NULL REFERENCES graphs(id),  -- which graph this node belongs to
    name     TEXT NOT NULL,           -- from <name> in XML
    PRIMARY KEY (id, graph_id)        -- id only needs to be unique within a graph
);

-- Stores directed edges between nodes
CREATE TABLE edges (
    id        TEXT NOT NULL,          -- from <id> in XML e.g. "e1"
    graph_id  TEXT NOT NULL REFERENCES graphs(id),
    from_node TEXT NOT NULL,          -- corresponds to <from> in XML
    to_node   TEXT NOT NULL,          -- corresponds to <to> in XML
    cost      FLOAT NOT NULL DEFAULT 0.0,  -- optional in XML, defaults to 0
    PRIMARY KEY (id, graph_id),
    FOREIGN KEY (from_node, graph_id) REFERENCES nodes(id, graph_id),
    FOREIGN KEY (to_node, graph_id)   REFERENCES nodes(id, graph_id)
);

-- Index for fast lookup of edges by their starting node (used in path queries)
CREATE INDEX idx_edges_from ON edges(graph_id, from_node);