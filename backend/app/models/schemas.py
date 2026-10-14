"""
Pydantic schemas matching the frontend TypeScript types.
Uses camelCase aliases so JSON keys match the React frontend exactly.
"""
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


# ── Helper to convert snake_case → camelCase ────────────
def _to_camel(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(w.capitalize() for w in parts[1:])


class _CamelModel(BaseModel):
    """Base model that serialises fields as camelCase."""
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=_to_camel,
    )


# ── Certificate ─────────────────────────────────────────

class PositionBox(_CamelModel):
    x: float
    y: float
    w: float
    h: float


class CertificateFieldSchema(_CamelModel):
    name: Optional[str] = None
    expected_value: Optional[str] = None
    extracted_value: Optional[str] = None
    match_status: Optional[str] = None      # 'match' | 'mismatch' | 'review'
    confidence: Optional[float] = None
    match_type: Optional[str] = None        # 'exact' | 'fuzzy' | 'vocabulary' | 'coordinate'
    reason: Optional[str] = None


class LayoutRegionSchema(_CamelModel):
    name: Optional[str] = None
    status: Optional[str] = None            # 'match' | 'position_difference' | 'anomaly'
    expected_position: Optional[PositionBox] = None
    actual_position: Optional[PositionBox] = None
    deviation: Optional[float] = None


class StudentRecordSchema(_CamelModel):
    roll_number: Optional[str] = None
    english_name: Optional[str] = None
    hindi_name: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    date_of_issue: Optional[str] = None
    cgpa: Optional[str] = None
    convocation_number: Optional[str] = None


class CertificateSchema(_CamelModel):
    id: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[str] = None
    file_type: Optional[str] = None
    upload_time: Optional[str] = None
    student_record: Optional[StudentRecordSchema] = None
    fields: Optional[list[CertificateFieldSchema]] = None
    layout_regions: Optional[list[LayoutRegionSchema]] = None
    overall_confidence: Optional[float] = None
    status: Optional[str] = None            # 'verified' | 'requires_review' | 'pending' | 'rejected'
    review_reason: Optional[str] = None


# ── Verification Pipeline ───────────────────────────────

class VerificationStepSchema(_CamelModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None            # 'pending' | 'processing' | 'completed' | 'warning' | 'error'
    detail: Optional[str] = None


class VerificationPipelineSchema(_CamelModel):
    certificate_id: Optional[str] = None
    steps: Optional[list[VerificationStepSchema]] = None
    current_step: Optional[int] = None
    is_complete: Optional[bool] = None


# ── Review ──────────────────────────────────────────────

class ReviewItemSchema(_CamelModel):
    certificate_id: Optional[str] = None
    student_name: Optional[str] = None
    roll_number: Optional[str] = None
    degree: Optional[str] = None
    flagged_fields: Optional[list[CertificateFieldSchema]] = None
    overall_confidence: Optional[float] = None
    review_reason: Optional[str] = None
    submitted_at: Optional[str] = None
    status: Optional[str] = None


class ReviewActionSchema(_CamelModel):
    decision: Optional[str] = None          # 'approve' | 'reject' | 'further_review'
    notes: Optional[str] = None
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[str] = None


# ── Dashboard ───────────────────────────────────────────

class DashboardStatsSchema(_CamelModel):
    total_certificates: Optional[int] = None
    verified: Optional[int] = None
    requires_review: Optional[int] = None
    pending: Optional[int] = None


class RecentVerificationSchema(_CamelModel):
    id: Optional[str] = None
    student_name: Optional[str] = None
    roll_number: Optional[str] = None
    degree: Optional[str] = None
    status: Optional[str] = None
    confidence: Optional[float] = None
    date: Optional[str] = None


# ── Generic responses ───────────────────────────────────

class UploadResponseSchema(_CamelModel):
    certificate_id: str
    status: str
    message: str


class ReviewResponseSchema(_CamelModel):
    success: bool
    updated_status: str
