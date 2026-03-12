# tucows-takehome-2026
TODO

"You want Docker version 20+ and Docker Compose version 2+."


clairejanke@Claires-MacBook-Air tucows-takehome-2026 % docker --version
docker compose version
Docker version 24.0.6, build ed223bc
Docker Compose version v2.22.0-desktop.2

`pytest tests/ -v`  to run tests

docker compose down -v
docker compose up --build

You can test the queries by using curl in the command line, eg:

```
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      { "paths": { "start": "a", "end": "e" } },
      { "cheapest": { "start": "a", "end": "e" } },
      { "cheapest": { "start": "a", "end": "h" } }
    ]
  }'
```

Alternatively, you can visit http://localhost:8000/docs and call the query from the UI there:
```
{
  "queries": [
    { "paths": { "start": "a", "end": "e" } },
    { "cheapest": { "start": "a", "end": "e" } },
    { "cheapest": { "start": "a", "end": "h" } }
  ]
}
```

Using xml.etree.ElementTree for xml parsing library - it's available by default in python, and the xml is pretty similar and predictable.

the parser assumes one graph per XML file per the spec, but could be extended to support a wrapper element for multiple graphs.



In case we want to support querying multiple graphs in the future, we store graphs in their own table and include graph ids in the records for nodes and edges. The API, though, assumes only one graph.

Propose a normalized SQL schema to model these graphs in PostgreSQL
using standard SQL data types only. Briefly explain each attribute and relationship, inline comments are fine.


## Cycle Detection

A standalone SQL query for detecting cycles in a graph is provided in `db/cycle_detection.sql`.

To test it:
1. Temporarily insert a cycle into the seed data:

    INSERT INTO edges (id, graph_id, from_node, to_node, cost)
    VALUES ('e8', 'g0', 'e', 'a', 1.0);

2. Rebuild the project

    docker compose down -v
    docker compose up --build

3. Connect to the database using preferred tool, eg TablePlus

4. Run the query on the database





