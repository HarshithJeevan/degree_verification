"""
Confidence scoring and verdict routing.

Maps the notebook's PASS/REVIEW/FAIL statuses to the frontend's
VerificationStatusType and computes an overall confidence score.
"""


# ── Status mapping ──────────────────────────────────────
# Notebook status  →  Frontend VerificationStatusType
STATUS_MAP = {
    "PASS":   "verified",
    "REVIEW": "requires_review",
    "FAIL":   "rejected",
}

# Notebook field status  →  Frontend FieldMatchStatus
FIELD_STATUS_MAP = {
    "PASS":   "match",
    "REVIEW": "review",
    "FAIL":   "mismatch",
}


def map_status(notebook_status: str) -> str:
    """Map notebook verdict (PASS/REVIEW/FAIL) to frontend status."""
    return STATUS_MAP.get(notebook_status, "pending")


def map_field_status(notebook_field_status: str) -> str:
    """Map notebook field result to frontend field match status."""
    return FIELD_STATUS_MAP.get(notebook_field_status, "review")


def compute_overall_confidence(field_results: list[dict]) -> float:
    """
    Calculate an overall confidence percentage from per-field results.

    Each field_result dict should have a 'similarity' key (0-100 float).
    Returns the weighted average, or 0.0 if no fields.
    """
    if not field_results:
        return 0.0

    total = sum(f.get("similarity", 0.0) for f in field_results)
    return round(total / len(field_results), 1)


def determine_verdict(field_results: list[dict]) -> str:
    """
    Aggregate per-field statuses into a single verdict.
    Logic (from notebook's overall()):
      - If ANY field is FAIL → 'FAIL'
      - Else if ANY field is REVIEW → 'REVIEW'
      - Else → 'PASS'
    """
    statuses = [f.get("status", "REVIEW") for f in field_results]

    if "FAIL" in statuses:
        return "FAIL"
    if "REVIEW" in statuses:
        return "REVIEW"
    return "PASS"


def build_review_reason(field_results: list[dict]) -> str | None:
    """Build a human-readable review reason from flagged fields."""
    flagged = [f for f in field_results if f.get("status") != "PASS"]
    if not flagged:
        return None

    reasons = []
    for f in flagged:
        name = f.get("field", "Unknown")
        note = f.get("note", "")
        reasons.append(f"{name}: {note}" if note else name)

    return "; ".join(reasons)
