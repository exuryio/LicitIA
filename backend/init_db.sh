#!/bin/bash
# Helper script to initialize the database with Alembic

echo "Running Alembic migrations..."
alembic upgrade head

echo "Database initialized successfully!"

