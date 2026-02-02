#!/bin/bash

# Quick Start Script for Dashboard V2

echo "🌍 Seismic Fractal Analysis Dashboard V2"
echo "=========================================="
echo ""

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not activated!"
    echo "Activating .venv..."
    source .venv/bin/activate
fi

echo "✅ Using Python: $(which python)"
echo "✅ Streamlit version: $(streamlit --version 2>&1 | head -n 1)"
echo ""

# Display available dashboards
echo "Available Dashboards:"
echo "  1. app.py (Original) - Port 8501"
echo "  2. app_v2.py (Enhanced) - Port 8503"
echo ""

# Check what's running
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "📊 app.py already running on port 8501"
else
    echo "   app.py not running"
fi

if lsof -Pi :8503 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "📊 app_v2.py already running on port 8503"
else
    echo "   app_v2.py not running"
fi

echo ""
echo "To start Dashboard V2:"
echo "  streamlit run app_v2.py --server.port 8503"
echo ""
echo "To run both simultaneously:"
echo "  Terminal 1: streamlit run app.py --server.port 8501"
echo "  Terminal 2: streamlit run app_v2.py --server.port 8503"
echo ""
