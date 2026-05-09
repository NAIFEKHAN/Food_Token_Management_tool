"""Admin API routes (JWT-protected)."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import Response
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..models import Student, TokenLog
from ..schemas import AdminLoginIn, VerifyTokenIn, StudentOut
from ..security import create_token, require_admin
from ..excel_io import import_students_from_excel, export_students_to_excel

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/login")
async def admin_login(payload: AdminLoginIn):
    if payload.username != settings.ADMIN_USERNAME or payload.password != settings.ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    return {
        "access_token": create_token(subject=payload.username, role="admin"),
        "token_type": "bearer",
    }


@router.get("/stats")
async def stats(_: dict = Depends(require_admin), db: Session = Depends(get_db)):
    total = db.query(Student).count()
    veg = db.query(Student).filter(Student.food_type == "Veg").count()
    nonveg = db.query(Student).filter(Student.food_type == "Non-Veg").count()
    not_selected = db.query(Student).filter(Student.food_type.is_(None)).count()
    used = db.query(Student).filter(Student.token_status == "Used").count()
    unused = db.query(Student).filter(
        Student.token_id.isnot(None), Student.token_status == "Unused"
    ).count()
    return {
        "total": total, "veg": veg, "non_veg": nonveg,
        "not_selected": not_selected, "used": used, "unused": unused,
    }


@router.get("/students")
async def list_students(_: dict = Depends(require_admin), db: Session = Depends(get_db),
                        q: Optional[str] = Query(None),
                        food: Optional[str] = Query(None)):
    query = db.query(Student)
    if q:
        like = f"%{q.strip()}%"
        query = query.filter(or_(Student.name.ilike(like), Student.roll_no.ilike(like)))
    if food in {"Veg", "Non-Veg"}:
        query = query.filter(Student.food_type == food)
    elif food == "None":
        query = query.filter(Student.food_type.is_(None))
    rows = query.order_by(Student.roll_no.asc()).all()
    return [StudentOut.model_validate(r).model_dump() for r in rows]


@router.post("/upload-excel")
async def upload_excel(_: dict = Depends(require_admin),
                       db: Session = Depends(get_db),
                       file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Please upload an .xlsx file")
    content = await file.read()
    try:
        inserted, skipped = import_students_from_excel(content, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"inserted": inserted, "skipped_duplicates": skipped}


@router.get("/export-excel")
async def export_excel(_: dict = Depends(require_admin), db: Session = Depends(get_db)):
    data = export_students_to_excel(db)
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="students_tokens.xlsx"'},
    )


@router.post("/verify-token")
async def verify_token(payload: VerifyTokenIn,
                       _: dict = Depends(require_admin),
                       db: Session = Depends(get_db)):
    token_id = payload.token_id.strip()
    student = db.query(Student).filter(Student.token_id == token_id).first()
    if not student:
        return {"status": "invalid", "message": "Invalid Token"}
    if student.token_status == "Used":
        db.add(TokenLog(student_id=student.id, token_id=token_id,
                        action="DUPLICATE_ATTEMPT"))
        db.commit()
        return {
            "status": "already_used", "message": "Already Used",
            "name": student.name, "roll_no": student.roll_no, "food_type": student.food_type,
        }
    student.token_status = "Used"
    db.add(TokenLog(student_id=student.id, token_id=token_id, action="USED"))
    db.commit()
    return {
        "status": "valid", "message": "Valid Token",
        "name": student.name, "roll_no": student.roll_no, "food_type": student.food_type,
    }
