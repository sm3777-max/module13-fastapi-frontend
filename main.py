from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base

# --- CRITICAL FIX START ---
# We MUST import models here. This forces SQLAlchemy to "load" the User and 
# Calculation classes so it knows what tables to create.
from app import models 
# --- CRITICAL FIX END ---

from app.routers import user_routes, calc_routes

# Create database tables
# Because we imported 'models' above, this will now create 'users' and 'calculations'
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount the static folder for HTML/CSS/JS
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Register the API routers
app.include_router(user_routes.router)
app.include_router(calc_routes.router)

@app.get("/")
def read_root():
    return {"message": "Go to /static/register.html or /static/login.html"}