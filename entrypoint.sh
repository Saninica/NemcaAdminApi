#!/usr/bin/env bash

# Run Alembic migrations
alembic upgrade head

# Start the FastAPI app
uvicorn "src.main:app" --host "0.0.0.0" --port 8002