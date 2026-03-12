from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import get_connection, release_connection
from app.graph import build_adjacency_list, find_all_paths, find_cheapest_path

app = FastAPI()

_cache = {"edges": None}

# --- Request/Response Models ---

class PathQuery(BaseModel):
    start: str
    end: str

class CheapestQuery(BaseModel):
    start: str
    end: str

class Query(BaseModel):
    paths: PathQuery | None = None
    cheapest: CheapestQuery | None = None

class QueryRequest(BaseModel):
    queries: list[Query]

# --- Database Helpers ---

def load_edges_from_db() -> list[dict]:
    """Load all edges from the database, if not already loaded."""
    # Cache edges so we don't need to repeatedly go to the db for follow-up queries
    if _cache["edges"] is not None:
        return _cache["edges"]

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, from_node, to_node, cost FROM edges")
        rows = cursor.fetchall()
        _cache["edges"] = [
            {"id": row[0], "from": row[1], "to": row[2], "cost": row[3]}
            for row in rows
        ]
        return _cache["edges"]
    finally:
        release_connection(conn)

# --- Endpoints ---

@app.get("/health") # FastAPI will run this function for any GET /health request
def health_check():
    """Simple endpoint to verify the API is running."""
    return {"status": "ok"}

@app.post("/query")
def query(request: QueryRequest):
    """Answer path queries against the graph stored in the database."""
    edges = load_edges_from_db()
    adjacency = build_adjacency_list(edges)

    answers = []
    for q in request.queries:
        if q.paths is not None:
            paths = find_all_paths(adjacency, q.paths.start, q.paths.end)
            answers.append({
                "paths": {
                    "from": q.paths.start,
                    "to": q.paths.end,
                    "paths": paths if paths else False
                }
            })
        elif q.cheapest is not None:
            path = find_cheapest_path(adjacency, q.cheapest.start, q.cheapest.end)
            answers.append({
                "cheapest": {
                    "from": q.cheapest.start,
                    "to": q.cheapest.end,
                    "path": path if path is not None else False
                }
            })
        else:
            raise HTTPException(status_code=400, detail="Each query must have either 'paths' or 'cheapest'")

    return {"answers": answers}