import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone

# Configuration
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    """
    Verifies a plain-text password against a hashed password.
    """
    # Bcrypt requires bytes, not strings
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    
    # Check the password
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)

def get_password_hash(password):
    """
    Hashes a plain-text password using bcrypt.
    """
    # Convert password to bytes
    pwd_bytes = password.encode('utf-8')
    
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    
    # Return as string for storage in database
    return hashed_password.decode('utf-8')

def create_access_token(data: dict):
    """
    Creates a JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt