FROM python:3.10-slim

# --- FIX: Install postgresql-client for the wait script ---
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*
# ---------------------------------------------------------

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files (including main.py, app/, and wait-for-db.sh)
COPY . .