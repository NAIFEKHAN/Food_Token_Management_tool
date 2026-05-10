"""FastAPI application entrypoint."""
import os
from contextlib import asynccontextmanager

<<<<<<< HEAD
=======

>>>>>>> 051ae550d2fa224873ff91c9d2bbe9f3bcd366c7
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

<<<<<<< HEAD

=======
>>>>>>> 051ae550d2fa224873ff91c9d2bbe9f3bcd366c7
from .config import settings
from .database import Base, engine, SessionLocal
from .excel_io import import_students_from_path
from .routers import student, admin, pages


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Optional: auto-import students from Excel on startup
    if settings.STUDENTS_EXCEL_PATH and os.path.exists(settings.STUDENTS_EXCEL_PATH):
        db = SessionLocal()
        try:
            inserted, skipped = import_students_from_path(settings.STUDENTS_EXCEL_PATH, db)
            print(f"[startup] Excel import: inserted={inserted} skipped={skipped}")
        except Exception as e:  # pragma: no cover
            print(f"[startup] Excel import failed: {e}")
        finally:
            db.close()
    yield


app = FastAPI(title=settings.EVENT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=False,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(pages.router)
app.include_router(student.router)
app.include_router(admin.router)

<<<<<<< HEAD

=======
@app.get("/")
async def root():
    return {"message": "Server is running"}
>>>>>>> 051ae550d2fa224873ff91c9d2bbe9f3bcd366c7
@app.get("/api/health")
async def health():
    return {"ok": True, "event": settings.EVENT_NAME}
