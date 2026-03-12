WITH RECURSIVE cycle_search AS (
    -- Base case: start at every node (one row per edge in the graph)
    SELECT
        e.graph_id,
        e.from_node AS start_node,
        e.to_node AS current_node,
        ARRAY[e.from_node] AS visited, -- track visited nodes to avoid infinite loops
        e.to_node = e.from_node AS cycle_found  -- handle edge case to detect self loops
    FROM edges e

    UNION ALL

    -- Recursive case: follow edges from current node
    SELECT
        cs.graph_id,
        cs.start_node,
        e.to_node AS current_node,
        cs.visited || e.from_node,                -- append from_node to list of those visited
        e.to_node = cs.start_node AS cycle_found  -- stop if we're back at the start node => cycle
    FROM edges e
    JOIN cycle_search cs
        ON e.graph_id = cs.graph_id
        AND e.from_node = cs.current_node
    WHERE NOT cs.cycle_found
        AND NOT (e.from_node = ANY(cs.visited)) -- infinite loop check
)
-- Note: graph_id is omitted from results as the API assumes a single graph at a time.
-- To support multiple graphs, add graph_id to the SELECT and WHERE clauses.
SELECT DISTINCT start_node, visited || current_node AS cycle_path -- append current node to visited list then output as cycle path
FROM cycle_search
WHERE cycle_found;