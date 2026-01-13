import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Vercel Blob Storage Configuration
BLOB_READ_WRITE_TOKEN = os.getenv("BLOB_READ_WRITE_TOKEN")

# AI Model Configuration (Ollama)
OLLAMA_MODEL_ID = os.getenv("OLLAMA_MODEL_ID", "llama3.2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Scanner Configuration
ROOT_SCAN_FOLDER = os.getenv("ROOT_SCAN_FOLDER", "njmtech-blob-api")


def validate_config():
    """Validates that all required environment variables are set."""
    required_vars = [
        "BLOB_READ_WRITE_TOKEN",
    ]
    missing_vars = [var for var in required_vars if not globals()[var]]
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )
