import os
from psycopg2 import pool

# Read the database URL from the environment variable set in docker-compose.yml
DATABASE_URL = os.environ.get("DATABASE_URL")

# A connection pool that maintains between 1 and 10 connections to Postgres.
# Created once when the module is first imported, reused across all requests.
connection_pool = pool.SimpleConnectionPool(1, 10, dsn=DATABASE_URL)

def get_connection():
    """Borrow a connection from the pool."""
    return connection_pool.getconn()

def release_connection(conn):
    """Return a connection to the pool when done."""
    connection_pool.putconn(conn)