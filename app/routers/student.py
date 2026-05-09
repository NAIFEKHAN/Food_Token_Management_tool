"""Student-facing API routes."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..models import Student, TokenLog
from ..schemas import StudentLoginIn, FoodSelectIn, TokenOut
from ..security import create_token, require_student
from ..qr_utils import generate_qr_data_url
from ..pdf_utils import build_token_pdf

router = APIRouter(prefix="/api/student", tags=["student"])


def _next_token_id(db: Session) -> str:
    """Generate the next sequential token id like FT-2026-001."""
    count = db.query(Student).filter(Student.token_id.isnot(None)).count()
    return f"FT-{settings.EVENT_YEAR}-{count + 1:03d}"


@router.post("/login")
async def student_login(payload: StudentLoginIn, db: Session = Depends(get_db)):

    print("Entered Roll:", payload.roll_no)

    student = db.query(Student).filter(
        Student.roll_no.ilike(payload.roll_no.strip())
    ).first()

    print("Student Found:", student)

    if not student:
        raise HTTPException(status_code=401, detail="Invalid roll number")

    # Password = Roll Number
    if payload.password.strip() != student.roll_no.strip():
        raise HTTPException(status_code=401, detail="Invalid password")
    token = create_token(subject=student.roll_no, role="student")
    return {
        "access_token": token,
        "token_type": "bearer",
        "name": student.name,
        "roll_no": student.roll_no,
        "has_selected": student.food_type is not None,
    }


@router.post("/select-food")
async def select_food(payload: FoodSelectIn,
                      student: Student = Depends(require_student),
                      db: Session = Depends(get_db)):
    if payload.food_type not in {"Veg", "Non-Veg"}:
        raise HTTPException(status_code=400, detail="food_type must be 'Veg' or 'Non-Veg'")
    if student.food_type:
        raise HTTPException(status_code=400, detail="Selection already submitted; cannot change")

    student.food_type = payload.food_type
    student.token_id = _next_token_id(db)
    student.qr_code = generate_qr_data_url(student.token_id)
    student.token_status = "Unused"
    db.add(TokenLog(student_id=student.id, token_id=student.token_id,
                    action="GENERATED", note=payload.food_type))
    db.commit()
    db.refresh(student)
    return {"ok": True, "token_id": student.token_id}


@router.get("/token", response_model=TokenOut)
async def my_token(student: Student = Depends(require_student)):
    if not student.token_id:
        raise HTTPException(status_code=404, detail="No token yet — select food first")
    return TokenOut(
        name=student.name, roll_no=student.roll_no,
        food_type=student.food_type, token_id=student.token_id,
        qr_code=student.qr_code, event_name=settings.EVENT_NAME,
    )


@router.get("/token.pdf")
async def my_token_pdf(student: Student = Depends(require_student)):
    if not student.token_id:
        raise HTTPException(status_code=404, detail="No token yet — select food first")
    pdf = build_token_pdf(
        event_name=settings.EVENT_NAME,
        name=student.name, roll_no=student.roll_no,
        food_type=student.food_type, token_id=student.token_id,
        qr_data_url=student.qr_code,
    )
    return Response(content=pdf, media_type="application/pdf", headers={
        "Content-Disposition": f'attachment; filename="{student.token_id}.pdf"'
    })
