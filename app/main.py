# in app/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Import all our new modules
from . import crud, models, schemas, database

# --- THIS IS NEW ---
# This command tells SQLAlchemy to create all the tables defined in
# app/models.py (like 'users' and 'calculations') if they don't
# already exist in the database.
models.Base.metadata.create_all(bind=database.engine)
# --- END NEW ---

app = FastAPI()

# --- THIS IS YOUR NEW SECURE USER ENDPOINT ---
@app.post("/users/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    
    # Check if a user with this email already exists
    db_user_email = crud.get_user_by_email(db, email=user.email)
    if db_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    
    # Check if a user with this username already exists
    db_user_username = crud.get_user_by_username(db, username=user.username)
    if db_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken."
        )
    
    # If all checks pass, create the new user
    return crud.create_user(db=db, user=user)
# --- END NEW ENDPOINT ---


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Calculator (Module 10)"}

# (You can add your calculator endpoints here later,
# but now they will be linked to a user_id)