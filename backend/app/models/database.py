"""
SQLAlchemy ORM models for the SQLite database.
"""
from sqlalchemy import Column, Integer, Float, Text, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.config import DATABASE_URL

Base = declarative_base()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency — yields a DB session and closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Tables ──────────────────────────────────────────────

class Student(Base):
    __tablename__ = "students"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    roll_number  = Column(Text, unique=True, nullable=False, index=True)
    english_name = Column(Text, nullable=False)
    hindi_name   = Column(Text)
    programme    = Column(Text)
    degree       = Column(Text)
    branch       = Column(Text)
    honours      = Column(Text)
    minors       = Column(Text)


class HindiVocab(Base):
    __tablename__ = "hindi_vocab"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    category     = Column(Text, nullable=False)       # 'prog', 'disc', 'minor', 'hon'
    english_term = Column(Text, nullable=False)
    hindi_term   = Column(Text, nullable=False)


class CertificateRecord(Base):
    __tablename__ = "certificates"

    id                   = Column(Text, primary_key=True)
    file_name            = Column(Text)
    file_path            = Column(Text)
    file_size            = Column(Integer)
    file_type            = Column(Text)
    upload_time          = Column(Text)
    roll_number          = Column(Text, ForeignKey("students.roll_number"), nullable=True)
    overall_confidence   = Column(Float)
    status               = Column(Text, default="pending")          # verified | requires_review | pending | rejected
    review_reason        = Column(Text)
    verification_result  = Column(Text)                             # JSON blob of full field-level results
    reviewed_by          = Column(Text)
    reviewed_at          = Column(Text)
    review_notes         = Column(Text)
