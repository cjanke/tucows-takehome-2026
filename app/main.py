from fastapi import FastAPI
from app.database import get_connection, release_connection

app = FastAPI()

@app.get("/health") # FastAPI will run this function for any GET /health request
def health_check():
    """Simple endpoint to verify the API is running."""
    return {"status": "ok"}