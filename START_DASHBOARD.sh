#!/bin/bash
# Quick start script for the dashboard

echo "==================================================================="
echo "🚀 Starting LicitIA Dashboard"
echo "==================================================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "   Creating from .env.example..."
    cp .env.example .env
    echo "   ✅ Please edit .env and add your configuration"
    echo ""
fi

echo "📋 Steps to view tenders in dashboard:"
echo ""
echo "1️⃣  Start the system:"
echo "   docker-compose -f docker/docker-compose.yml up --build"
echo ""
echo "2️⃣  Wait for services to start (about 30 seconds)"
echo ""
echo "3️⃣  Fetch tenders (in another terminal):"
echo "   cd backend"
echo "   python3 -c \"from app.services.tender_ingestion import fetch_and_store_new_tenders; fetch_and_store_new_tenders()\""
echo ""
echo "4️⃣  Open browser:"
echo "   http://localhost:3000"
echo ""
echo "5️⃣  Set filters:"
echo "   - Fecha desde: 01/08/2025"
echo "   - Fecha hasta: (today)"
echo "   - Click 'Buscar'"
echo ""
echo "==================================================================="
echo "📝 See HOW_TO_USE_DASHBOARD.md for detailed instructions"
echo "==================================================================="

