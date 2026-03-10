# Breaking down how to handle problem

Here's the plan I'd suggest tackling in order:

Project structure + Docker setup — get the skeleton in place
XML parsing + validation (Part 1 & 2)
SQL schema (Part 3)
REST API with path queries (Part 5) — "find all paths" and "cheapest path"
Cycle detection SQL query (Part 4)
Tests + README + AI_USAGE.md

The cycle detection SQL is the trickiest part intellectually but doesn't block the rest, so we'll do it near the end.
For the core libraries, I'd recommend:

FastAPI — modern, clean REST API framework, easy to explain
psycopg2 or asyncpg — Postgres driver
xml.etree.ElementTree — Python's built-in XML parser (simple to justify: no extra dependency)
Docker + docker-compose — for Postgres + your service

# Discussing project structure

```
graph-challenge/
├── docker-compose.yml          # Postgres + API services
├── Dockerfile                  # Python API container
├── requirements.txt
├── README.md
├── AI_USAGE.md
│
├── db/
│   └── schema.sql              # Table definitions + migration
│
├── app/
│   ├── main.py                 # FastAPI app + /query endpoint
│   ├── models.py               # Pydantic models for request/response JSON
│   ├── database.py             # Postgres connection logic
│   ├── parser.py               # XML parsing + validation
│   └── graph.py                # Path-finding algorithms (DFS, Dijkstra)
│
├── tests/
│   ├── test_parser.py
│   └── test_graph.py
│
└── sample/
    └── sample_graph.xml        # A sample XML file to test with
```

A few decisions worth noting:

parser.py and graph.py are separated so the algorithms are independently testable without a database
db/schema.sql is a plain SQL file — simple, no ORM needed for a challenge this size
sample/ gives reviewers something concrete to run against

Let's start filling it in piece by piece. I'd suggest this order for today:

docker-compose.yml + Dockerfile + requirements.txt — get the environment working first
db/schema.sql — define the Postgres schema
parser.py — XML parsing and validation
graph.py — path-finding algorithms
app/ — FastAPI wiring
Tests, README, AI_USAGE.md

Shall we start with the Docker + requirements setup? It's mostly mechanical but getting it right early means you can actually run and test each piece as we build it rather than debugging everything at the end.

# Docker environment set up


"Claude initially suggested explicitly including Pydantic in requirements.txt (it's used by fast api) but I pushed back and we removed it since we don't use it directly."

Adding my own comments to dockerfile, requirements.txt, etc because I haven't set up too many projects with docker and I'm learning.