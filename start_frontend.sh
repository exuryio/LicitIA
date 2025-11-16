#!/bin/bash
# Quick script to start frontend

cd /Users/exury/Desktop/LicitIA/Licitia/frontend

echo "🚀 Starting Frontend..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start dev server
echo "✅ Starting React dev server..."
echo "   Dashboard: http://localhost:5173 (or check terminal for actual port)"
echo ""
npm run dev

