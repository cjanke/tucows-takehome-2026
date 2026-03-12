WITH RECURSIVE cycle_search AS (
    -- Base case: start at every node
    SELECT
        e.graph_id,
        e.from_node AS start_node,
        e.to_node AS current_node,
        ARRAY[e.from_node] AS visited,
        FALSE AS cycle_found
    FROM edges e

    UNION ALL

    -- Recursive case: follow edges from current node
    SELECT
        cs.graph_id,
        cs.start_node,
        e.to_node AS current_node,
        cs.visited || e.from_node AS visited,  -- append current node to visited path
        e.to_node = ANY(cs.visited) AS cycle_found  -- cycle if we've seen this node before
    FROM edges e
    JOIN cycle_search cs
        ON e.graph_id = cs.graph_id
        AND e.from_node = cs.current_node
    WHERE NOT cs.cycle_found  -- stop recursing once cycle is found
        AND NOT (e.from_node = ANY(cs.visited))  -- stop if we've already visited this node
)
SELECT DISTINCT graph_id, start_node
FROM cycle_search
WHERE cycle_found;