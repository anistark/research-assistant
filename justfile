# Research Assistant - justfile

# Create data directory and setup
setup:
    mkdir -p data
    mkdir -p chroma_db
    cp backend/.env.example backend/.env
    @echo "📝 Created .env files and directories."
    @echo "📁 Place your sample_chunks.json in the data/ directory."

install:
    #!/usr/bin/env bash
    if ! command -v uv &> /dev/null; then
        echo "📦 Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source $HOME/.cargo/env
    fi
    echo "🐍 Python version: $(python --version)"
    echo "📦 Installing Python dependencies..."
    cd backend && uv pip install -r requirements.txt
    cd ..
    echo "📦 Installing Node dependencies..."
    cd frontend && npm install

# Start backend server
backend:
    cd backend && python -m src.main

# Start frontend
frontend:
    cd frontend && npm start

# Load sample data
data:
    cd scripts && python load_json_data.py

# Run API tests
test:
    cd scripts && python test_endpoints.py

# Start everything locally using tmux
dev:
    tmux new-session -d -s research 'just backend'
    tmux split-window -h 'just frontend'
    tmux attach-session -t research

# Docker compose - start full stack
docker:
    docker-compose up --build

# Docker compose - start in background
docker-up:
    docker-compose up -d --build

# Docker compose - start without rebuild
docker-start:
    docker-compose up

# Docker compose - stop services
docker-stop:
    docker-compose down

# Docker compose - stop and remove volumes
docker-down:
    docker-compose down -v

# Build Docker images only
docker-build:
    docker-compose build

# Load data into Docker backend
docker-data:
    @echo "🔄 Loading sample data into Docker backend..."
    sleep 5  # Wait for backend to be ready
    curl -X PUT "http://localhost:8000/api/upload" \
        -H "Content-Type: application/json" \
        -d @data/sample_chunks.json \
        && echo "✅ Data loaded successfully" \
        || echo "❌ Data loading failed"

# Clean generated files
clean:
    rm -rf chroma_db/
    rm -rf frontend/build/
    rm -rf frontend/node_modules/
    rm -rf backend/__pycache__/
    rm -rf backend/src/__pycache__/
    rm -rf scripts/__pycache__/

# Clean everything including Docker
clean-all: clean docker-down
    docker system prune -f
    docker volume prune -f
