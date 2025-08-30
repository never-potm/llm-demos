import os
from dotenv import load_dotenv

# load .env from repo root
ROOT = os.path.dirname(os.path.dirname(__file__)) if __file__.endswith(".py") else os.getcwd()
load_dotenv(os.path.join(ROOT, ".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OLLAMA_API = os.getenv("OLLAMA_API", "http://localhost:11434")
