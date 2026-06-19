from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports"

LOG_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("API Key:", GEMINI_API_KEY)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

MAX_FILE_SIZE_MB = int(
    os.getenv("MAX_FILE_SIZE_MB", "100")
)

ALLOWED_EXTENSIONS = [".pdf"]

GEMINI_MODEL = "gemini-2.5-flash"
