# tucows-takehome-2026

# Prerequisites

- Docker version 20+
- Docker Compose version 2+."
- Pytest (for running the unit tests)

# How to run the program

The app is built within a Docker container. Basic seed data for the db (see `db/02_seed.sql`) is handled automatically.
For the initial build, run `docker compose up --build` in your terminal at the root directory.

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

# Project Structure
```
<tucows-takehome-2026/
├── app/
│   ├── database.py       # PostgreSQL connection pool
│   ├── graph.py          # Path-finding algorithms (DFS, Dijkstra)
│   ├── main.py           # FastAPI app, Pydantic models, and /query endpoint
│   └── parser.py         # XML parsing and validation
├── db/
│   ├── 01_schema.sql        # Table definitions
│   ├── 02_seed.sql          # Sample graph data
│   └── cycle_detection.sql  # Standalone cycle detection query
├── sample/
│   ├── sample_graph.xml  # Full sample graph for testing
│   ├── simple_graph.xml  # Minimal two-node graph
│   └── ...               # Invalid graphs for parser error testing
├── tests/
│   ├── test_graph.py     # Unit tests for path-finding algorithms
│   └── test_parser.py    # Unit tests for XML parser
├── docker-compose.yml    # Defines API and PostgreSQL services
├── Dockerfile            # Python API container definition
└── requirements.txt      # Python dependencies
```

# Schema

The graph is modeled across three tables in PostgreSQL:
- `graphs` — stores graph metadata (id, name)
    - Note - not necessary for this version of the API, but good to have for the future if functionality is expanded to handle multiple graphs.
- `nodes` — stores nodes, each belonging to a graph via foreign key
- `edges` — stores directed edges between nodes, with an optional cost defaulting to 0

See `db/01_schema.sql` for full definitions and inline commentary.

# Design decisions and commentary

Normally credentials would be stored in a .env file and NOT in plain text in `docker-compose.yml`, but since this is a toy problem we're doing plain text for ease of testing for everyone.

After seeking input from Claude, I decided to use `xml.etree.ElementTree` for the XML parsing library - it's available by default for python, and the XML we'll be working with is simple and predictable.

I'm not as familiar with python frameworks, so I also followed Claude's advice for using FastAPI as the API framework with Pydantic models that automatically parse the incoming JSON request body into Python objects and validate it. Upon independently researching both, they seem like popular options in the community and suitable for a simple project.

The Pydantic query models are defined in main.py for simplicity given the single endpoint. If there were more models, they would go in a dedicated models.py file.

The parser assumes one graph per XML file per the spec, but could be extended to support a wrapper element for multiple graphs.

We use depth-first search to find all paths, since it's well-suited to that and more space efficient than BFS.

For cheapest path, Dijkstra's algorithm is the standard solution and it works fine for our case because we don't have to worry about negative edge weights (in which case we would use the Bellman-Ford algorithm).

In case we want to support querying multiple graphs in the future, we store graphs in their own table and include reference graph ids in the records for nodes and edges. The API, though, assumes only one graph for simplicity.

