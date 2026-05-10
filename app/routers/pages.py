"""HTML page routes (Jinja2 templates)."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..config import settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def _ctx(request: Request, **kw):
    return {"request": request, "event_name": settings.EVENT_NAME, **kw}


@router.get("/", response_class=HTMLResponse)
async def student_login_page(request: Request):
    return templates.TemplateResponse(
        request,
        "student_login.html",
        _ctx(request)
    )


@router.get("/food", response_class=HTMLResponse)
async def food_page(request: Request):
    return templates.TemplateResponse(
    request,
    "food_select.html",
    _ctx(request)
    )


@router.get("/token", response_class=HTMLResponse)
async def token_page(request: Request):
    return templates.TemplateResponse(
    request,
    "token.html",
    _ctx(request)
    )


@router.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse(
    request,
    "admin_login.html",
    _ctx(request)
    )


@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard_page(request: Request):
    return templates.TemplateResponse(
    request,
    "admin_dashboard.html",
    _ctx(request)
    )


@router.get("/admin/scanner", response_class=HTMLResponse)
async def admin_scanner_page(request: Request):
    return templates.TemplateResponse(
    request,
    "admin_scanner.html",
    _ctx(request)
    )
