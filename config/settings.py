import os

from dotenv import load_dotenv


load_dotenv()


OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

if not OLLAMA_MODEL:
    raise ValueError("OLLAMA_MODEL is not configured.")