# Install poetry if not already installed
function Install-Poetry {
    if (-not (Get-Command poetry -ErrorAction SilentlyContinue)) {
        python -m pip install poetry
        Write-Output "Poetry installed successfully."
    } else {
        Write-Output "Poetry is already installed."
    }
}

# Update pip and ensurepip
python -m ensurepip --upgrade
python -m pip install --upgrade pip
Install-Poetry

# Locate poetry executable
$POETRY_BIN = "$(python -m site --user-base)\Scripts\poetry.exe"

# Install dependencies
function Install-Dependencies {
    # create the virtual environment inside the project directory using poetry
    & $POETRY_BIN config virtualenvs.in-project true
    & $POETRY_BIN install --no-root
}

# Update dependencies
function Update-Dependencies {
    & $POETRY_BIN update
}

# Start the FastAPI application
function Start-Server {
    param (
        [string]$env
    )

    if ($env -ne "dev" -and $env -ne "prod") {
        Write-Output "Invalid configuration name. Usage: {dev|prod}"
        exit 1
    }

    # Set the APP_ENV for the entire Gunicorn process
    $env:APP_ENV = $env

    # Use Python to get settings, parse JSON, and extract values
    $settings = & $POETRY_BIN run python -c @"
import json
from com.crack.snap.make.di import container

settings = container.settings()

# Print each value on a new line
print(settings.host)
print(settings.port)
print(str(settings.debug).lower())
"@

    # Read the output lines into PowerShell variables
    $settingsLines = $settings -split "`n"
    $host = $settingsLines[0].Trim()
    $port = $settingsLines[1].Trim()
    $debug = $settingsLines[2].Trim()

    if ($debug -eq "true") {
        & $POETRY_BIN run gunicorn "com.crack.snap.make.app:app" `
            --workers 1 `
            --worker-class uvicorn.workers.UvicornWorker `
            --bind "$host:$port" `
            --reload `
            --log-level debug `
            --timeout 200 `
            --preload
    } else {
        & $POETRY_BIN run gunicorn "com.crack.snap.make.app:app" `
            --workers 4 `
            --worker-class uvicorn.workers.UvicornWorker `
            --bind "$host:$port" `
            --log-level info `
            --timeout 300 `
            --preload
    }
}

function Clear-ChromaDB {
    & $POETRY_BIN run python -m com.crack.snap.make.vectorizer --clear
}

function Vectorize {
    param (
        [string]$pathOfDocuments
    )

    & $POETRY_BIN run python -m com.crack.snap.make.vectorizer "$pathOfDocuments" -or { Write-Output "Vectorizing documents failed"; exit 1 }
}

param (
    [string]$action,
    [string]$env
)

switch ($action) {
    "setup" {
        Write-Output "Setting up project dependencies..."
        Install-Dependencies
        Write-Output "Project setup complete."
    }
    "update" {
        Write-Output "Updating project dependencies..."
        Update-Dependencies
        Write-Output "Project dependencies updated."
    }
    "ingest" {
        if (-not $env) {
            Write-Output "Error: Missing path_of_documents"
            exit 1
        }
        Write-Output "Vectorizing documents from $env..."
        Vectorize $env
        Write-Output "Documents vectorized..."
    }
    "clean_db" {
        Write-Output "Clearing ChromaDB..."
        Clear-ChromaDB
        Write-Output "ChromaDB cleared."
    }
    "start" {
        Write-Output "Starting FastAPI server..."
        Start-Server $env
    }
    default {
        Write-Output "Invalid command. Usage: {setup|update|start} {dev|prod}"
        exit 1
    }
}
