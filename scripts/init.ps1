# PowerShell Script for Windows Setup

# Check Prerequisites
function Check-Prerequisites {
    Write-Host "Checking Prerequisites..."
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "Python is not installed. Please install Python before continuing."
        exit
    }
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Host "Docker is not installed. Please install Docker before continuing."
        exit
    }
}

# Create Python Virtual Environment
function Create-Venv {
    Write-Host "Creating Python virtual environment..."
    python -m venv venv
}

# Install Dependencies
function Install-Dependencies {
    Write-Host "Installing dependencies..."
    .\venv\Scripts\activate
    pip install -r requirements.txt
}

# Set Up Environment File
function Setup-Environment {
    Write-Host "Setting up environment file..."
    $envContent = "DATABASE_URL=mysql://user:password@mysql:3306/dbname`
`nKAFKA_URL=kafka:9092`
`nMONGODB_URL=mongodb://mongo:27017/"
    Set-Content -Path .env -Value $envContent
}

# Start Docker Containers
function Start-Docker {
    Write-Host "Starting Docker containers..."
    docker-compose up -d
}

# Initialize Databases
function Initialize-Databases {
    Write-Host "Initializing databases..."
    # Add commands to initialize databases if necessary, e.g., creating tables
}

# Main Execution
Check-Prerequisites
Create-Venv
Install-Dependencies
Setup-Environment
Start-Docker
Initialize-Databases
