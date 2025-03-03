import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3-8b-8192")


if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")
