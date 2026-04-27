import os
from dotenv import load_dotenv

load_dotenv()

API_URL   = os.getenv("API_URL",    "").strip()
API_KEY   = os.getenv("API_KEY",    "").strip()
MODEL_NAME = os.getenv("MODEL_NAME", "").strip()

if not API_URL:
    raise ValueError("API_URL is missing in .env file")
if not MODEL_NAME:
    raise ValueError("MODEL_NAME is missing in .env file")