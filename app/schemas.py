# in app/schemas.py

from pydantic import BaseModel, EmailStr, ConfigDict, model_validator # <-- Import model_validator
from datetime import datetime
from .logic import OperationType # Import our new Enum

# --- User Schemas (from Module 10) ---

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime
    
    # Use ConfigDict for modern Pydantic
    model_config = ConfigDict(from_attributes=True)


# --- Calculation Schemas (NEW for Module 11) ---

class CalculationBase(BaseModel):
    a: float
    b: float
    type: OperationType # Use the Enum for validation

class CalculationCreate(CalculationBase):
    
    # --- THIS IS THE FIX ---
    # We use a model_validator (mode='after') to check fields
    # after they have all been individually validated.
    
    @model_validator(mode='after')
    def check_division_by_zero(self) -> 'CalculationCreate':
        """
        After all fields are validated, check for division by zero.
        """
        if self.type == OperationType.DIVIDE and self.b == 0:
            raise ValueError("Cannot divide by zero")
        return self
    # --- END FIX ---

class CalculationRead(CalculationBase):
    id: int
    result: float
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)