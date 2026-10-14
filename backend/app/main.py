"""
FastAPI application entry point.

Run with:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import FRONTEND_URL
from app.routers import upload, verification, certificates, dashboard, review

app = FastAPI(
    title="Degree Certificate Verification API",
    description="Backend API for IIT Gandhinagar Degree Certificate Verification System — CS-202 (STTCSE)",
    version="1.0.0",
)

# ── CORS ────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ─────────────────────────────────────────────
# NOTE: upload must be registered BEFORE certificates because they share
# the /api/certificates prefix. FastAPI matches routes in registration order,
# so /upload (exact) must come before /{cert_id} (parameterized).
app.include_router(dashboard.router,     prefix="/api/dashboard",     tags=["Dashboard"])
app.include_router(upload.router,        prefix="/api/certificates",  tags=["Upload"])
app.include_router(certificates.router,  prefix="/api/certificates",  tags=["Certificates"])
app.include_router(verification.router,  prefix="/api/verification",  tags=["Verification"])
app.include_router(review.router,        prefix="/api/review",        tags=["Review"])


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "degree-certificate-verification-api"}
