"""
Verification pipeline status endpoint.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db, CertificateRecord
from app.models.schemas import VerificationPipelineSchema, VerificationStepSchema

router = APIRouter()

# The 9 stages of the verification pipeline
PIPELINE_STEPS = [
    {"id": 1, "name": "PDF Parsing",             "description": "Extracting text layers and character data from the PDF"},
    {"id": 2, "name": "Font Detection",           "description": "Identifying Hindi (Kruti Dev / Ajay) and English font streams"},
    {"id": 3, "name": "Text Extraction",          "description": "Converting legacy font encodings to Unicode"},
    {"id": 4, "name": "Roll Number Detection",    "description": "Extracting roll number via pattern matching"},
    {"id": 5, "name": "Database Lookup",          "description": "Retrieving student record from roster database"},
    {"id": 6, "name": "English Field Matching",   "description": "Comparing English name, degree, branch against records"},
    {"id": 7, "name": "Hindi Field Matching",     "description": "Multi-tier Hindi comparison (exact → bag → soft → OCR)"},
    {"id": 8, "name": "Tesseract OCR (if needed)","description": "Running OCR fallback for ambiguous Hindi text"},
    {"id": 9, "name": "Scoring & Verdict",        "description": "Aggregating field confidences and determining final status"},
]


@router.get("/{cert_id}/status", response_model=VerificationPipelineSchema)
def get_verification_status(cert_id: str, db: Session = Depends(get_db)):
    """
    Return the current state of the verification pipeline for a certificate.
    Since verification runs synchronously for now, the pipeline is either
    fully complete or still pending.
    """
    cert = db.query(CertificateRecord).filter(CertificateRecord.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    is_done = cert.status != "pending"

    steps = []
    for step_def in PIPELINE_STEPS:
        if is_done:
            step_status = "completed"
        else:
            step_status = "pending"

        steps.append(VerificationStepSchema(
            id=step_def["id"],
            name=step_def["name"],
            description=step_def["description"],
            status=step_status,
        ))

    # If verification finished with issues, mark the last step accordingly
    if is_done and cert.status == "requires_review":
        steps[-1].status = "warning"
        steps[-1].detail = cert.review_reason or "Some fields require human review"
    elif is_done and cert.status == "rejected":
        steps[-1].status = "error"
        steps[-1].detail = cert.review_reason or "Verification failed"

    return VerificationPipelineSchema(
        certificate_id=cert_id,
        steps=steps,
        current_step=len(steps) if is_done else 0,
        is_complete=is_done,
    )
