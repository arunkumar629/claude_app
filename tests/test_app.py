import os
import sqlite3
import tempfile

import pytest

from app import app, init_db, DATABASE


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create a test client with a temporary database."""
    db_path = str(tmp_path / "test.db")
    monkeypatch.setattr("app.DATABASE", db_path)
    with app.test_client() as client:
        with app.app_context():
            conn = sqlite3.connect(db_path)
            conn.execute(
                "CREATE TABLE IF NOT EXISTS users ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT NOT NULL, "
                "age INTEGER NOT NULL)"
            )
            conn.commit()
            conn.close()
        yield client


def test_index_get(client):
    """GET / should return the form page."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Add User" in response.data


def test_index_post_redirects(client):
    """POST / with valid data should redirect."""
    response = client.post("/", data={"name": "Alice", "age": "30"})
    assert response.status_code == 302


def test_users_page_empty(client):
    """GET /users should show empty state when no users exist."""
    response = client.get("/users")
    assert response.status_code == 200
    assert b"No users found" in response.data


def test_add_and_view_user(client):
    """Adding a user via POST should make it visible on /users."""
    client.post("/", data={"name": "Bob", "age": "25"})
    response = client.get("/users")
    assert response.status_code == 200
    assert b"Bob" in response.data
    assert b"25" in response.data


def test_add_multiple_users(client):
    """Multiple users should all appear on the users page."""
    client.post("/", data={"name": "Alice", "age": "30"})
    client.post("/", data={"name": "Bob", "age": "25"})
    response = client.get("/users")
    assert b"Alice" in response.data
    assert b"Bob" in response.data
