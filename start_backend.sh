#!/bin/bash
# Quick script to start backend

cd /Users/exury/Desktop/LicitIA/Licitia/backend

echo "🚀 Starting Backend..."
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.installed" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Check .env
if [ ! -f "../.env" ]; then
    echo "⚠️  .env file not found!"
    echo "   Creating from .env.example..."
    cp ../.env.example ../.env
    echo "   ✅ Please edit ../.env and add your configuration"
fi

# Run migrations
echo "🗄️  Running database migrations..."
alembic upgrade head

# Start server
echo "✅ Starting FastAPI server on http://localhost:8000"
echo "   API docs: http://localhost:8000/docs"
echo ""
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

