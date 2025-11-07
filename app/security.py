# in app/security.py

import bcrypt

def verify_password(plain_password, hashed_password):
    """
    Verifies a plain-text password against a hashed password.
    
    Args:
        plain_password (str): The password to check.
        hashed_password (str): The stored hash from the database.
        
    Returns:
        bool: True if the password matches, False otherwise.
    """
    # Convert both to bytes for bcrypt
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    # bcrypt.checkpw handles the salt comparison automatically
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)

def get_password_hash(password):
    """
    Hashes a plain-text password.
    
    Args:
        password (str): The plain-text password to hash.
        
    Returns:
        str: The hashed password, decoded as a string.
    """
    # Convert password to bytes
    password_bytes = password.encode('utf-8')
    
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # Decode back to a string to store in the database
    return hashed_password_bytes.decode('utf-8')