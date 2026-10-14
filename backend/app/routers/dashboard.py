"""
Dashboard endpoints — aggregate stats and recent verifications.
"""
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.database import get_db, CertificateRecord, Student
from app.models.schemas import DashboardStatsSchema, RecentVerificationSchema

router = APIRouter()


@router.get("/stats", response_model=DashboardStatsSchema)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Return aggregate counts by verification status."""
    total     = db.query(func.count(CertificateRecord.id)).scalar() or 0
    verified  = db.query(func.count(CertificateRecord.id)).filter(CertificateRecord.status == "verified").scalar() or 0
    review    = db.query(func.count(CertificateRecord.id)).filter(CertificateRecord.status == "requires_review").scalar() or 0
    pending   = db.query(func.count(CertificateRecord.id)).filter(CertificateRecord.status == "pending").scalar() or 0

    return DashboardStatsSchema(
        total_certificates=total,
        verified=verified,
        requires_review=review,
        pending=pending,
    )


@router.get("/recent", response_model=list[RecentVerificationSchema])
def get_recent_verifications(limit: int = 10, db: Session = Depends(get_db)):
    """Return the most recent certificate verification records."""
    rows = (
        db.query(CertificateRecord)
        .order_by(CertificateRecord.upload_time.desc())
        .limit(limit)
        .all()
    )
    results: list[RecentVerificationSchema] = []
    for cert in rows:
        # Look up student name & degree from the students table
        student = db.query(Student).filter(Student.roll_number == cert.roll_number).first()
        results.append(RecentVerificationSchema(
            id=cert.id,
            student_name=student.english_name if student else None,
            roll_number=cert.roll_number,
            degree=student.degree if student else None,
            status=cert.status,
            confidence=cert.overall_confidence,
            date=cert.upload_time,
        ))
    return results
