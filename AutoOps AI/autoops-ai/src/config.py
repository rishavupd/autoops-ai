import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

DATA_PATH = "data/invoices.csv"
OUTPUT_DIR = "outputs"

TODAY = "2026-04-28"

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing. Please add it in your .env file.")