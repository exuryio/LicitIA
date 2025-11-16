#!/bin/bash
# Quick script to start everything with Docker

echo "==================================================================="
echo "🐳 Starting LicitIA with Docker"
echo "==================================================================="
echo ""

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker is not running!"
    echo ""
    echo "Please:"
    echo "1. Open Docker Desktop application"
    echo "2. Wait for it to fully start (whale icon in menu bar)"
    echo "3. Run this script again"
    echo ""
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "   Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "   ✅ Created .env - Please edit it with your settings"
    else
        echo "   ❌ .env.example not found!"
        exit 1
    fi
    echo ""
fi

echo "🚀 Starting all services..."
echo ""
echo "This will start:"
echo "  - PostgreSQL database (port 5432)"
echo "  - Backend API (port 8000)"
echo "  - Frontend Dashboard (port 3000)"
echo ""
echo "Press CTRL+C to stop all services"
echo ""
echo "==================================================================="
echo ""

cd "$(dirname "$0")"
docker-compose -f docker/docker-compose.yml up --build

