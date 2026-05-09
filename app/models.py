"""ORM models: Student and TokenLog."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from .database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    roll_no = Column(String(50), unique=True, nullable=False, index=True)
    # Per spec: password equals roll number. Stored to allow future change.
    password = Column(String(100), nullable=False)
    food_type = Column(String(20), nullable=True)        # "Veg" | "Non-Veg" | None
    token_id = Column(String(30), unique=True, nullable=True, index=True)
    qr_code = Column(Text, nullable=True)                # base64 PNG data URL
    token_status = Column(String(20), default="Unused") # "Unused" | "Used"
    created_at = Column(DateTime, default=datetime.utcnow)

    logs = relationship("TokenLog", back_populates="student", cascade="all, delete-orphan")


class TokenLog(Base):
    __tablename__ = "token_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    token_id = Column(String(30), nullable=False)
    action = Column(String(40), nullable=False)   # e.g. "GENERATED", "USED", "DUPLICATE_ATTEMPT"
    note = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="logs")
