"""Excel import/export helpers using pandas + openpyxl."""
from io import BytesIO
from typing import Tuple

import pandas as pd
from sqlalchemy.orm import Session

from .models import Student


# Accept several common header spellings
NAME_KEYS = {"name", "student name", "student"}
ROLL_KEYS = {"roll no", "rollno", "roll_no", "roll number", "rollnumber", "roll"}


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename = {}
    for col in df.columns:
        key = str(col).strip().lower()
        if key in NAME_KEYS:
            rename[col] = "name"
        elif key in ROLL_KEYS:
            rename[col] = "roll_no"
    return df.rename(columns=rename)


def import_students_from_excel(file_bytes: bytes, db: Session) -> Tuple[int, int]:
    """Import students. Returns (inserted, skipped_duplicates)."""
    df = pd.read_excel(BytesIO(file_bytes), engine="openpyxl")
    df = _normalize_columns(df)
    if "name" not in df.columns or "roll_no" not in df.columns:
        raise ValueError("Excel must contain 'Name' and 'Roll No' columns")

    inserted = 0
    skipped = 0
    for _, row in df.iterrows():
        name = str(row["name"]).strip() if pd.notna(row["name"]) else ""
        roll = str(row["roll_no"]).strip() if pd.notna(row["roll_no"]) else ""
        if not name or not roll:
            continue
        existing = db.query(Student).filter(Student.roll_no == roll).first()
        if existing:
            skipped += 1
            continue
        db.add(Student(name=name, roll_no=roll, password=roll))
        inserted += 1
    db.commit()
    return inserted, skipped


def import_students_from_path(path: str, db: Session) -> Tuple[int, int]:
    with open(path, "rb") as f:
        return import_students_from_excel(f.read(), db)


def export_students_to_excel(db: Session) -> bytes:
    """Export all students with token info to an .xlsx byte buffer."""
    rows = db.query(Student).order_by(Student.roll_no.asc()).all()
    data = [{
        "Name": s.name,
        "Roll No": s.roll_no,
        "Food": s.food_type or "",
        "Token": s.token_id or "",
        "Status": s.token_status or "Unused",
    } for s in rows]
    df = pd.DataFrame(data, columns=["Name", "Roll No", "Food", "Token", "Status"])
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Students")
    return buf.getvalue()
