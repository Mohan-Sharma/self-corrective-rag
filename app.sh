#!/bin/bash

# Install poetry if not already installed
function install_poetry {
    if ! command -v poetry &> /dev/null
    then
        python -m pip install poetry
        echo "Poetry installed successfully."
    else
        echo "Poetry is already installed."
    fi
}

# Update pip and ensurepip
python -m ensurepip --upgrade
python -m pip install --upgrade pip
install_poetry

# Locate poetry executable
POETRY_BIN=$(python3 -m site --user-base)/bin/poetry

# Install deps
function install_dependencies {
    # create the virtual environment inside the project directory using poetry
    $POETRY_BIN config virtualenvs.in-project true
    $POETRY_BIN install --no-root
}

# Update deps
function update_dependencies {
    $POETRY_BIN update
}

# Start the FastAPI application
function start_server_bak {
    if [ "$1" != "dev" ] && [ "$1" != "prod" ]; then
        echo "Invalid configuration name. Usage: $0 start {dev|prod}"
        exit 1
    fi
    $POETRY_BIN run python -m com.crack.snap.make.app $1
}

function start_server {
    if [ "$1" != "dev" ] && [ "$1" != "prod" ]; then
        echo "Invalid configuration name. Usage: $0 {dev|prod}"
        exit 1
    fi

    # Set the APP_ENV for the entire Gunicorn process
    export APP_ENV="$1"

    # Use Python to get settings, parse JSON, and extract values
    settings=$($POETRY_BIN run python -c "
import json
from com.crack.snap.make.di import container

settings = container.settings()

# Print each value on a new line
print(settings.host)
print(settings.port)
print(str(settings.debug).lower())
")

# Read the output lines into bash variables
IFS=$'\n' read -d '' -r host port debug <<< "$settings"


    if [ "$debug" = "true" ]; then
        $POETRY_BIN run gunicorn "com.crack.snap.make.app:app" \
            --workers 1 \
            --worker-class uvicorn.workers.UvicornWorker \
            --bind $host:$port \
            --reload \
            --log-level debug \
            --timeout 200 \
            --preload
    else
        $POETRY_BIN run gunicorn "com.crack.snap.make.app:app" \
            --workers 4 \
            --worker-class uvicorn.workers.UvicornWorker \
            --bind $host:$port \
            --log-level info \
            --timeout 300 \
            --preload
    fi
}

function clear_chromadb {
    $POETRY_BIN run python -m com.crack.snap.make.vectorizer --clear
}

function vectorize {
    local path_of_documents=$1
    $POETRY_BIN run python -m com.crack.snap.make.vectorizer "${path_of_documents}" || { echo "Vectorizing documents failed"; exit 1; }
}

case "$1" in
    setup)
        echo "Setting up project dependencies..."
        install_dependencies
        echo "Project setup complete."
        ;;
    update)
        echo "Updating project dependencies..."
        update_dependencies
        echo "Project dependencies updated."
        ;;
    ingest)
        if [ -z "$2" ]; then
            echo "Error: Missing path_of_documents"
            exit 1
        fi
        echo "Vectorizing documents from $2..."
        vectorize "$2"
        echo "Documents vectorized..."
        ;;
    clean_db)
        echo "Setting up project dependencies..."
        clear_chromadb
        echo "ChromaDB cleared."
        ;;
    start)
        echo "Starting FastAPI server..."
        start_server $2
        ;;
    *)
        echo "Invalid command. Usage: $0 {setup|update|start} {dev|prod}"
        exit 1
esac
