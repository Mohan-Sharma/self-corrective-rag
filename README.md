# Self Corrective RAG App

## Starter template to build any rag app using FastAPI, Poetry, Python ^3.11, Pydantic and Dependency Injector
## Getting Started

This application uses Poetry for dependency management. The `app.sh` script will handle the installation of pip (if not already installed), Poetry (if not already installed), configure Poetry to use an in-project virtual environment, install project dependencies.

### Prerequisites

- Python 3.11 or higher
- Download and install [Ollama](https://ollama.com/download)
- [How to pull serve Ollama and pull llama3 model from Ollama](https://github.com/ollama/ollama)
- If you install Ollama via brew, don't forget to start Ollama using `Ollama serve` and pull the llama3 model using `Ollama pull llama3`. You don't need to do `Ollama serve` if using Ollama desktop app

### Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. Make the setup script executable (if not already done):
    ```sh
    chmod +x app.sh
    ```
3. Install dependencies and create virtual environment:
    ```sh
    . ./app.sh setup
   ```
4. To vectorize the text or pdfs, you need to run the following command:
    ```sh
    . ./app.sh ingest absolute_directory_path_of_pdf_files
    ```
5. To start the app with the desired environment, either `dev` or `prod`. This will start the app at `http://localhost:5500`. Then you can start chatting with your data
    ```sh
    . ./app.sh start dev  # For development environment
    ```
6. To remove the vector DB, you can run the following command:
    ```sh
    . ./app.sh clean_db
    ```
7. To use web seach, get your api key from [Tavily](https://app.tavily.com/) and put it in `.env` file

The script does the following:
- Ensure pip is installed and up to date using `pip3`.
- Install Poetry if it is not already installed.
- Configure Poetry to create a virtual environment inside the project directory.
- Install all dependencies using Poetry.
- Set the configuration environment variable.
- Start the FastAPI application using Poetry's environment.
 ```

### Troubleshooting

If you encounter any issues, please check the following:
- Ensure Python 3.11 or higher is installed.
- Ensure the `app.sh` script has executable permissions.

For any further assistance, feel free to open an issue on the repository. I would be happy to help

Running In windows should be pretty similar, all you need is to 
1. Install python
2. Install Ollama, run Ollama and pull the llama3 model
3. Convert the app.sh to powershell script

### Notes
At present, this app demonstrate how to vectorize pdfs, adopt to your usecase
