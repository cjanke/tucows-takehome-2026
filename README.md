# tucows-takehome-2026

# Prerequisites

- Docker version 20+
- Docker Compose version 2+."
- Pytest (for running the unit tests)

# How to run the program

The app is built within a Docker container.
For the initial build, run `docker compose down -v` in your terminal at the root directory:

For subsequent builds, wipe the existing data before running:

```
docker compose down -v
docker compose up --build
```

# Testing

## Unit tests

Run `pytest tests/ -v` in the terminal.

## Submitting API queries

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

## Cycle Detection

A standalone SQL query for detecting cycles in a graph is provided in `db/cycle_detection.sql`.

To test it:
1. Temporarily insert a cycle into the seed data:

    INSERT INTO edges (id, graph_id, from_node, to_node, cost)
    VALUES ('e8', 'g0', 'e', 'a', 1.0);

  Note: these lines are already present in db/seed.sql (see very bottom of file), commented out for easy testing.

2. Rebuild the project

    docker compose down -v
    docker compose up --build

3. Connect to the database using preferred tool, eg TablePlus

4. Copy and paste the query into the database tool and run it. The output should look like this:

| start_node | cycle_path |
|------------|------------|
| a | {a,b,e,a} |
| a | {a,a} |
| a | {a,e,a} |
| e | {e,a,c,e} |
| e | {e,a,e} |
| a | {a,c,e,a} |
| e | {e,a,b,e} |
| b | {b,e,a,b} |
| c | {c,e,a,c} |


# Design decisions and commentary

After seeking input from Claude, I decided to use `xml.etree.ElementTree` for the XML parsing library - it's available by default for python, and the XML we'll be working with is simple and predictable.

I'm not as familiar with python frameworks, so I also followed Claude's advice for using FastAPI as the API framework with Pydantic models that automatically parse the incoming JSON request body into Python objects and validate it. Upon independently researching both, they seem like popular options in the community and suitable for a simple project.

The Pydantic query models are defined in main.py for simplicity given the single endpoint. If there were more models, they would go in a dedicated models.py file.

The parser assumes one graph per XML file per the spec, but could be extended to support a wrapper element for multiple graphs.

We use depth-first search to find all paths, since it's well-suited to that and more space efficient than BFS.

For cheapest path, Dijkstra's algorithm is the standard solution and it works fine for our case because we don't have to worry about negative edge weights (in which case we would use the Bellman-Ford algorithm).

In case we want to support querying multiple graphs in the future, we store graphs in their own table and include reference graph ids in the records for nodes and edges. The API, though, assumes only one graph for simplicity.



TODO:
Propose a normalized SQL schema to model these graphs in PostgreSQL
using standard SQL data types only. Briefly explain each attribute and relationship, inline comments are fine.
(I don't know how best to do this in the readme, if it should be done in the readme or just in the schema.sql, etc.)






