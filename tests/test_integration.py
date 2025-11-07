# in tests/test_integration.py
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base
import pytest

# Use a test client
client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    """Fixture to create and clean up database tables for tests."""
    # Create the tables
    Base.metadata.create_all(bind=engine)
    yield SessionLocal()
    # Drop the tables after tests
    Base.metadata.drop_all(bind=engine)

def test_create_user_success(db):
    """Test creating a new user successfully."""
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data
    assert "password_hash" not in data # Check that hash isn't returned

def test_create_user_duplicate_email(db):
    """Test creating a user with a duplicate email."""
    # This user is created from the previous test
    response = client.post("/users/", json={
        "username": "newuser",
        "email": "test@example.com", # Duplicate email
        "password": "password123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered."

def test_create_user_duplicate_username(db):
    """Test creating a user with a duplicate username."""
    response = client.post("/users/", json={
        "username": "testuser", # Duplicate username
        "email": "new@example.com",
        "password": "password123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken."