# Module 12: Final Backend API (Users & Calculations)

This project completes the backend logic for the FastAPI Calculator. It integrates User Authentication (Registration/Login) and full CRUD (BREAD) operations for Calculations, backed by a PostgreSQL database.

## Project Features
* **User Authentication**: secure endpoints for `/users/register` and `/users/login`.
* **Calculation CRUD**: Complete API to Browse, Read, Edit, Add, and Delete calculations.
* **Database Integration**: Uses SQLAlchemy with a `User` and `Calculation` model (One-to-Many relationship).
* **Automated Testing**: Integration tests for API endpoints and database logic.
* **CI/CD**: GitHub Actions pipeline for automated testing and Docker Hub deployment.

---

## 🐳 How to Run with Docker
1.  Make sure you have Docker Desktop running.
2.  Clone this repository.
3.  From the project's root directory, run:
    ```bash
    docker compose up --build -d
    ```
4.  **Access the API Docs (Swagger UI):**
    Open your browser to **[http://localhost:8000/docs](http://localhost:8000/docs)** to manually test the endpoints.
5.  **Access pgAdmin:**
    Go to `http://localhost:5050` (Email: `admin@example.com`, Password: `admin`).

---

## 🧪 How to Run Tests Locally
Integration tests require a running database.

1.  **Start the database container:**
    ```bash
    docker compose up -d
    ```
2.  **Run pytest with the correct host:**
    ```bash
    POSTGRES_HOST=localhost pytest
    ```

---

## ship: Docker Hub Repository

The CI/CD pipeline automatically builds and pushes the Docker image for this project.

**Repository Link:** [https://hub.docker.com/r/sm3777/module12-fastapi-final](https://hub.docker.com/r/sm3777/module12-fastapi-final)