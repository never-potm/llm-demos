import os
from dotenv import load_dotenv

# load .env from repo root
ROOT = os.path.dirname(os.path.dirname(__file__)) if __file__.endswith(".py") else os.getcwd()
load_dotenv(os.path.join(ROOT, ".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAAI_MODEL_NAME = os.getenv("OPENAAI_MODEL_NAME", "gpt-5-nano")
OLLAMA_API = os.getenv("OLLAMA_API", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
