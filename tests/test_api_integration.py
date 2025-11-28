from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest

# --- CORRECT IMPORT ---
# Since main.py is now in the root folder, we import directly from 'main'
from main import app
# ----------------------

from app.database import SessionLocal, engine, Base
from app import crud, models

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """
    Fixture to create a clean database environment for tests.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_user_flow():
    """
    Test 1: Register a User
    Test 2: Login to get a token
    """
    # 1. Register
    reg_response = client.post("/users/register", json={
        "username": "integration_user",
        "email": "integration@test.com",
        "password": "securepassword"
    })
    assert reg_response.status_code == 200
    data = reg_response.json()
    assert data["email"] == "integration@test.com"
    assert "id" in data

    # 2. Login
    login_response = client.post("/users/login", data={
        "username": "integration@test.com", 
        "password": "securepassword"
    })
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_calculation_crud_flow():
    """
    Test the full lifecycle of a calculation (BREAD).
    """
    # 1. ADD (Create)
    # We assume User ID 1 exists from the previous test
    create_res = client.post("/calculations/", json={
        "a": 10, 
        "b": 5, 
        "type": "add"
    })
    assert create_res.status_code == 200
    data = create_res.json()
    calc_id = data["id"]
    assert data["result"] == 15.0

    # 2. READ (Get One)
    read_res = client.get(f"/calculations/{calc_id}")
    assert read_res.status_code == 200
    assert read_res.json()["id"] == calc_id

    # 3. EDIT (Update)
    update_res = client.put(f"/calculations/{calc_id}", json={
        "a": 10, 
        "b": 2, 
        "type": "divide"
    })
    assert update_res.status_code == 200
    assert update_res.json()["result"] == 5.0

    # 4. DELETE
    del_res = client.delete(f"/calculations/{calc_id}")
    assert del_res.status_code == 204