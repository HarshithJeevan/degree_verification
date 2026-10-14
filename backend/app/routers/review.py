"""
Review queue and review action endpoints.
"""
import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db, CertificateRecord, Student
from app.models.schemas import (
    ReviewItemSchema,
    ReviewActionSchema,
    ReviewResponseSchema,
    CertificateFieldSchema,
)

router = APIRouter()


@router.get("/queue", response_model=list[ReviewItemSchema])
def get_review_queue(db: Session = Depends(get_db)):
    """Return all certificates flagged for human review."""
    certs = (
        db.query(CertificateRecord)
        .filter(CertificateRecord.status.in_(["requires_review", "rejected"]))
        .order_by(CertificateRecord.upload_time.desc())
        .all()
    )

    items: list[ReviewItemSchema] = []
    for cert in certs:
        student = db.query(Student).filter(Student.roll_number == cert.roll_number).first()

        # Extract flagged fields from stored verification result
        flagged: list[CertificateFieldSchema] = []
        if cert.verification_result:
            try:
                data = json.loads(cert.verification_result)
                for f in data.get("fields", []):
                    if f.get("matchStatus") != "match":
                        flagged.append(CertificateFieldSchema(**f))
            except (json.JSONDecodeError, TypeError):
                pass

        items.append(ReviewItemSchema(
            certificate_id=cert.id,
            student_name=student.english_name if student else None,
            roll_number=cert.roll_number,
            degree=student.degree if student else None,
            flagged_fields=flagged if flagged else None,
            overall_confidence=cert.overall_confidence,
            review_reason=cert.review_reason,
            submitted_at=cert.upload_time,
            status=cert.status,
        ))

    return items


@router.post("/{cert_id}/action", response_model=ReviewResponseSchema)
def submit_review(cert_id: str, action: ReviewActionSchema, db: Session = Depends(get_db)):
    """Record a human review decision (approve / reject / further_review)."""
    cert = db.query(CertificateRecord).filter(CertificateRecord.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    decision_map = {
        "approve": "verified",
        "reject": "rejected",
        "further_review": "requires_review",
    }
    new_status = decision_map.get(action.decision, cert.status)

    cert.status       = new_status
    cert.reviewed_by  = action.reviewed_by
    cert.reviewed_at  = action.reviewed_at or datetime.now(timezone.utc).isoformat()
    cert.review_notes = action.notes
    db.commit()

    return ReviewResponseSchema(success=True, updated_status=new_status)
