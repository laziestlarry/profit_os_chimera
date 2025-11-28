#!/bin/bash
# Start Profit OS Chimera services

set -e

echo "🚀 Starting Profit OS Chimera v0.1.0"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python -c "from database.connection import init_db; init_db()"

# Start API
echo "Starting API server..."
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &

# Start Frontend (optional)
if [ "$1" == "--with-frontend" ]; then
    echo "Starting frontend dashboard..."
    streamlit run frontend/dashboard.py --server.port 8501 &
fi

echo "✅ Profit OS Chimera is running!"
echo "API: http://localhost:8000"
echo "API Docs: http://localhost:8000/api/docs"
if [ "$1" == "--with-frontend" ]; then
    echo "Frontend: http://localhost:8501"
fi

wait



