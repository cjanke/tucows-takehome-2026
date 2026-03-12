WITH RECURSIVE cycle_search AS (
    -- Base case: start at every node (one row per edge in the graph)
    SELECT
        e.graph_id,
        e.from_node AS start_node,
        e.to_node AS current_node,
        ARRAY[e.from_node] AS visited, -- track visited nodes to avoid infinite loops
        CASE                                    -- keep log of nodes in path to output at end
            WHEN e.to_node = e.from_node
            THEN ARRAY[e.from_node, e.to_node]
            ELSE ARRAY[]::text[]                -- initialize empty text array to hold path
        END AS cycle_path,
        e.to_node = e.from_node AS cycle_found  -- handle edge case to detect self loops
    FROM edges e

    UNION ALL

    -- Recursive case: follow edges from current node
    SELECT
        cs.graph_id,
        cs.start_node,
        e.to_node AS current_node,
        cs.visited || e.from_node,  -- append from node to list of those visited
        CASE
            WHEN e.to_node = cs.start_node  -- if the next node is the start node, we've found a cycle
            THEN cs.visited || e.from_node || e.to_node  -- append last nodes to list visited to complete the cycle path
            ELSE ARRAY[]::text[]
        END AS cycle_path,
        e.to_node = cs.start_node AS cycle_found
    FROM edges e
    JOIN cycle_search cs
        ON e.graph_id = cs.graph_id
        AND e.from_node = cs.current_node
    WHERE NOT cs.cycle_found
        AND NOT (e.from_node = ANY(cs.visited))
)
SELECT DISTINCT start_node, cycle_path
FROM cycle_search
WHERE cycle_found;