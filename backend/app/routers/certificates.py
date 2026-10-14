"""
Certificate detail endpoint — returns the full verification result.
"""
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db, CertificateRecord, Student
from app.models.schemas import (
    CertificateSchema,
    StudentRecordSchema,
    CertificateFieldSchema,
)

router = APIRouter()


@router.get("/{cert_id}", response_model=CertificateSchema)
def get_certificate(cert_id: str, db: Session = Depends(get_db)):
    """Return the full certificate object including field-level results."""
    cert = db.query(CertificateRecord).filter(CertificateRecord.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    # ── Build student record ────────────────────────────
    student_record = None
    if cert.roll_number:
        student = db.query(Student).filter(Student.roll_number == cert.roll_number).first()
        if student:
            student_record = StudentRecordSchema(
                roll_number=student.roll_number,
                english_name=student.english_name,
                hindi_name=student.hindi_name,
                degree=student.degree,
                branch=student.branch,
            )

    # ── Parse stored verification result JSON ───────────
    fields: list[CertificateFieldSchema] = []
    if cert.verification_result:
        try:
            result_data = json.loads(cert.verification_result)
            for f in result_data.get("fields", []):
                fields.append(CertificateFieldSchema(**f))
        except (json.JSONDecodeError, TypeError):
            pass

    return CertificateSchema(
        id=cert.id,
        file_name=cert.file_name,
        file_size=str(cert.file_size) if cert.file_size else None,
        file_type=cert.file_type,
        upload_time=cert.upload_time,
        student_record=student_record,
        fields=fields if fields else None,
        overall_confidence=cert.overall_confidence,
        status=cert.status,
        review_reason=cert.review_reason,
    )
