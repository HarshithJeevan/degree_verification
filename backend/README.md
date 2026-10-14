# Degree Certificate Verification — Backend

FastAPI backend for the IIT Gandhinagar Degree Certificate Verification System (CS-202, STTCSE).

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Make sure Tesseract OCR is installed with Hindi language support
#    Download: https://github.com/UB-Mannheim/tesseract/wiki
#    Update TESSERACT_CMD in .env if installed elsewhere

# 3. Initialize the database (imports Excel roster into SQLite)
python -m app.db.init_db

# 4. Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs available at: http://localhost:8000/docs

## Project Structure

```
backend/
├── app/
│   ├── main.py              ← FastAPI entry point
│   ├── config.py            ← Settings & environment variables
│   ├── models/
│   │   ├── schemas.py       ← Pydantic models (match frontend types)
│   │   └── database.py      ← SQLAlchemy ORM models
│   ├── routers/
│   │   ├── dashboard.py     ← GET /api/dashboard/stats & /recent
│   │   ├── upload.py        ← POST /api/certificates/upload
│   │   ├── verification.py  ← GET /api/verification/{id}/status
│   │   ├── certificates.py  ← GET /api/certificates/{id}
│   │   └── review.py        ← POST /api/review/{id}/action & GET /queue
│   ├── services/
│   │   ├── kruti_dev.py     ← Kruti Dev → Unicode transcoder
│   │   ├── hindi_utils.py   ← Hindi normalization & comparison
│   │   ├── pdf_parser.py    ← PDF text extraction & template parsing
│   │   ├── ocr_service.py   ← Tesseract OCR fallback
│   │   ├── roster.py        ← Student DB lookup
│   │   ├── verifier.py      ← Main verification pipeline
│   │   └── scoring.py       ← Confidence scoring & verdict routing
│   └── db/
│       ├── init_db.py       ← Excel → SQLite import script
│       └── degree_verify.db ← SQLite database (auto-generated)
├── uploads/                 ← Uploaded certificate files
├── requirements.txt
├── .env
└── README.md
```
