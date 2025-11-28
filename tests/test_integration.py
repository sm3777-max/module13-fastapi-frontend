import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# --- CORRECT IMPORT ---
from main import app
# ----------------------

from app.database import SessionLocal, engine, Base
from app import crud
from app.schemas import CalculationCreate
from app.logic import OperationType

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    """Fixture to set up a clean database for this test module."""
    Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()
    yield db_session
    db_session.close()
    Base.metadata.drop_all(bind=engine)

# --- USER TESTS ---

def test_create_user_success(db: Session):
    """Test creating a new user successfully via the /users/register endpoint."""
    response = client.post("/users/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"

def test_create_user_duplicate_email(db: Session):
    """Test creating a user with a duplicate email."""
    response = client.post("/users/register", json={
        "username": "newuser",
        "email": "test@example.com", # Duplicate email
        "password": "password123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

# --- CALCULATION TEST ---

def test_crud_create_calculation_for_user(db: Session):
    """
    Test creating a calculation record linked to a user.
    """
    # 1. Get the user we created in the first test
    user = crud.get_user_by_username(db, username="testuser")
    assert user is not None, "User 'testuser' not found in database"
    
    # 2. Define the calculation data
    calc_data = CalculationCreate(
        a=20,
        b=5,
        type=OperationType.DIVIDE
    )
    
    # 3. Use the CRUD function
    db_calc = crud.create_calculation(db=db, calc=calc_data, user_id=user.id)
    
    # 4. Verify result
    assert db_calc.id is not None
    assert db_calc.result == 4.0
    assert db_calc.user_id == user.id