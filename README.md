# Module 10: Secure FastAPI User Model & CI/CD

This project demonstrates a secure user model for a FastAPI application using SQLAlchemy and password hashing. It is built on the Module 9 project and adds a full CI/CD pipeline with GitHub Actions and Docker Hub.

## Project Features
* **Secure User Model**: SQLAlchemy `User` model with `username`, `email`, and `password_hash`.
* **Password Hashing**: Uses `bcrypt` for secure password hashing and verification.
* **Pydantic Schemas**: `UserCreate` and `UserRead` schemas to safely handle data.
* **CI/CD Pipeline**: Automates testing and deployment to Docker Hub.
* **Docker Compose**: Runs the full stack (FastAPI, PostgreSQL, pgAdmin).

---

## 🐳 How to Run with Docker
This is the easiest way to run the full application stack, including the database.

1.  Make sure you have Docker Desktop running.
2.  Clone this repository.
3.  From the project's root directory, run:
    ```bash
    docker-compose up --build
    ```
4.  The application will be running at **`http://127.0.0.1:8000`**.
5.  pgAdmin (database manager) will be available at **`http://127.0.0.1:5050`**.

---

## 🧪 How to Run Tests Locally
You can run the unit and integration tests on your local machine.

1.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  Install all dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run `pytest`:
    ```bash
    pytest
    ```
    *(Note: Integration tests may fail locally if you don't have a database running with the correct environment variables.)*

---

## 🚢 Docker Hub Repository

The CI/CD pipeline automatically builds and pushes the Docker image for this project to Docker Hub.

You can find the repository here:
**[https://hub.docker.com/r/sm3777-max/module10-fastapi-secure](https://hub.docker.com/r/sm3777-max/module10-fastapi-secure)**

---

## 🐍 How to Run Locally (Original Setup)
This method runs the app directly on your machine using a Python virtual environment.

1.  Clone the repository.
2.  Create and activate a virtual environment.
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    playwright install
    ```
4.  Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```