"""
Configuration settings for the Degree Certificate Verification backend.
Loads values from environment variables / .env file.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent          # backend/
PROJECT_ROOT = BASE_DIR.parent                             # degree_verify_not_github/
_upload_raw = os.getenv("UPLOAD_DIR", "uploads").lstrip("./\\")
UPLOAD_DIR = BASE_DIR / _upload_raw
DATABASE_PATH = BASE_DIR / "app" / "db" / "degree_verify.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

EXCEL_ROSTER_PATH = PROJECT_ROOT / os.getenv(
    "EXCEL_ROSTER_PATH",
    "Degree Verification_Convocation 2026 (1).xlsx"
)

# --- Tesseract ---
TESSERACT_CMD = os.getenv(
    "TESSERACT_CMD",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# --- Server / CORS ---
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# --- Verification thresholds (from notebook CONFIG) ---
COLUMN_GAP = float(os.getenv("COLUMN_GAP", "3.0"))
SPACE_GAP = float(os.getenv("SPACE_GAP", "0.25"))           # gap (x font size) → space between English chars
FUZZY_THRESHOLD = int(os.getenv("FUZZY_THRESHOLD", "85"))    # RapidFuzz minimum score
BAG_PASS_VOCAB = os.getenv("BAG_PASS_VOCAB", "true").lower() == "true"
USE_OCR = os.getenv("USE_OCR", "true").lower() == "true"
TESSDATA = os.getenv("TESSDATA", None)                       # folder of hin.traineddata if not system-wide

# Fixed template text that changes per convocation — update for each ceremony
DATE_HI = [
    "vkt chl twu nks gtkj NCchl dks laLFkku dh ;g",
    "eqnzk vafdr mikf/k iznku dh x;h",
]
DATE_EN = "on this Twentieth day of June Two Thousand Twenty Six"

# --- Ensure upload directory exists ---
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
