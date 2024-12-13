import pytest
import sqlite3
from src.utils.db_helpers import init_db_schema

@pytest.fixture
def setup_db():
    conn = sqlite3.connect("users.db")
    yield conn
    conn.close()

@pytest.fixture
def db_cursor(db_connection):
    return db_connection.cursor()