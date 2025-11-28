from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas, crud, database, security

# Create the router
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=schemas.UserRead)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Check if email already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Create the user
    return crud.create_user(db=db, user=user)

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # 1. Check if user exists and password is correct
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Create a REAL JWT Access Token
    access_token = security.create_access_token(data={"sub": user.email})
    
    # 3. Return the token
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "message": "Login successful"
    }