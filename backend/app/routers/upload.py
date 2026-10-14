"""
Upload endpoint — receives a certificate file and kicks off verification.
"""
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import UPLOAD_DIR
from app.models.database import get_db, CertificateRecord
from app.models.schemas import UploadResponseSchema
from app.services.verifier import run_verification

router = APIRouter()


@router.post("/upload", response_model=UploadResponseSchema)
def upload_certificate(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Accept a certificate PDF / image, save it, create a DB record,
    run the verification pipeline, and return the result status.
    """
    # ── Validate file type ──────────────────────────────
    allowed = {"application/pdf", "image/jpeg", "image/png", "image/jpg"}
    is_pdf = (
        file.content_type == "application/pdf"
        or (file.filename and file.filename.lower().endswith(".pdf"))
    )
    if not is_pdf:
        raise HTTPException(
            status_code=400,
            detail="Only PDF certificates with text layers are supported.",
        )

    # ── Save file to disk ───────────────────────────────
    cert_id = str(uuid.uuid4())[:12]
    safe_name = file.filename.replace(" ", "_") if file.filename else "certificate"
    save_name = f"{cert_id}_{safe_name}"
    save_path = UPLOAD_DIR / save_name

    contents = file.file.read()
    with open(save_path, "wb") as f:
        f.write(contents)

    # ── Create DB record ────────────────────────────────
    now = datetime.now(timezone.utc).isoformat()
    record = CertificateRecord(
        id=cert_id,
        file_name=file.filename,
        file_path=str(save_path),
        file_size=len(contents),
        file_type=file.content_type,
        upload_time=now,
        status="pending",
    )
    db.add(record)
    db.commit()

    # ── Run verification (synchronous for now) ──────────
    try:
        status = run_verification(cert_id, str(save_path), db)
    except Exception as e:
        # Don't crash the upload even if verification fails
        status = "pending"
        record.review_reason = f"Verification error: {e}"
        db.commit()

    return UploadResponseSchema(
        certificate_id=cert_id,
        status=status,
        message=f"Certificate uploaded and verification {'completed' if status != 'pending' else 'queued'}.",
    )
