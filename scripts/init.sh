#!/bin/bash

# Detect OS
case "$(uname)" in
    Darwin)
        OS="macOS"
        ;;
    Linux)
        OS="Linux"
        ;;
    *)
        echo "Unsupported OS: $(uname)"
        exit 1
        ;;
esac

echo "Detected OS: $OS"

# Check prerequisites
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.";
    exit 1;
fi

if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker.";
    exit 1;
fi

# Create Python virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Set up environment file
if [ ! -f ".env" ]; then
    echo "Setting up .env file..."
    cp .env.example .env
fi

# Start Docker containers
echo "Starting Docker containers..."
docker-compose up -d

# Initialize databases
echo "Initializing databases..."
# Assuming initialization scripts are provided in init.sql
docker exec -i <your_database_container_name> psql -U <your_username> -d <your_database> < init.sql

echo "Setup completed successfully!"