# Farewell Food Token Management System

Full-stack web app for managing food tokens at a college farewell event.

- **Backend:** FastAPI (async)
- **Database:** MySQL (SQLAlchemy ORM)
- **Frontend:** HTML + Bootstrap 5 + vanilla JS (served by FastAPI)
- **Excel:** pandas + openpyxl
- **QR generation:** `qrcode`
- **QR scanning:** `html5-qrcode` (browser)
- **PDF tokens:** reportlab
- **Auth:** JWT for admin, signed session token for students

---

## Features

- Roll-number-only student login (username = password = roll number)
- Auto-import students from Excel on startup (optional) **or** upload Excel from admin dashboard
- One-time Veg / Non-Veg selection per student
- Unique token IDs (`FT-2026-001`) with QR code
- Token display page with Print / Download PNG / Download PDF
- Admin login (default: `biher` / `biherit`)
- Admin dashboard:
  - Total students, Veg/Non-Veg counts, not-selected, used/unused tokens
  - Chart.js analytics
  - Searchable / filterable student table
  - Excel upload (bulk student import)
  - Excel export (full student + token data)
  - Mobile QR scanner using html5-qrcode (mark token as USED, prevent duplicates)

---

## Folder structure

```
farewell-food-token/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app, routes mounting, startup hooks
│   ├── config.py               # Settings (env vars)
│   ├── database.py             # SQLAlchemy engine + session
│   ├── models.py               # ORM models: Student, TokenLog
│   ├── schemas.py              # Pydantic schemas
│   ├── security.py             # JWT + admin/student auth dependencies
│   ├── excel_io.py             # Excel import/export with pandas + openpyxl
│   ├── qr_utils.py             # QR code generation
│   ├── pdf_utils.py            # PDF token generation (reportlab)
│   └── routers/
│       ├── __init__.py
│       ├── student.py          # /api/student/*
│       ├── admin.py            # /api/admin/*
│       └── pages.py            # HTML page routes
├── templates/                  # Jinja2 HTML templates
│   ├── base.html
│   ├── student_login.html
│   ├── food_select.html
│   ├── token.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   └── admin_scanner.html
├── static/
│   ├── css/style.css           # Black & gold theme
│   └── js/                     # Page-specific JS
├── data/                       # Generated exports + uploads
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup

### 1. Prerequisites

- Python 3.10+
- MySQL 8.x running locally (or anywhere reachable)

### 2. Create the database

```sql
CREATE DATABASE farewell_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Tables are created automatically by SQLAlchemy on first run.

### 3. Install & configure

```bash
cd farewell-food-token
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # then edit DB credentials
```

### 4. (Optional) Auto-import students at startup

Place an Excel file with columns `Name` and `Roll No` somewhere on disk and set:

```
STUDENTS_EXCEL_PATH=/absolute/path/to/students.xlsx
```

Or skip this and upload the Excel from the admin dashboard.

### 5. Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open:

- Student login:  http://localhost:8000/
- Admin login:    http://localhost:8000/admin/login

Default admin: **biher / biherit**

---

## Excel format (input)

| Name  | Roll No   |
|-------|-----------|
| Arun  | 22CS001   |
| Rahul | 22IT045   |

Upload from **Admin Dashboard → Upload Excel**, or set `STUDENTS_EXCEL_PATH`.

## Excel format (export)

| Name | Roll No | Food | Token | Status |

---

## API summary

| Method | Path                              | Auth        | Purpose                        |
|--------|-----------------------------------|-------------|--------------------------------|
| POST   | /api/student/login                | none        | Login with roll number         |
| POST   | /api/student/select-food          | student     | Pick Veg / Non-Veg (one-time)  |
| GET    | /api/student/token                | student     | Get own token + QR             |
| GET    | /api/student/token.pdf            | student     | Download PDF token             |
| POST   | /api/admin/login                  | none        | Admin JWT                      |
| GET    | /api/admin/stats                  | admin       | Dashboard analytics            |
| GET    | /api/admin/students               | admin       | List/search/filter students    |
| POST   | /api/admin/upload-excel           | admin       | Bulk import students           |
| GET    | /api/admin/export-excel           | admin       | Download updated Excel         |
| POST   | /api/admin/verify-token           | admin       | Mark scanned token as USED     |

---

## Notes

- Student "passwords" equal their roll number per spec — this is intentionally low-security and only suitable for a one-day event.
- Admin routes are JWT-protected; student routes use a signed session token stored in `localStorage`.
- Excel export is generated on demand from the live DB (always up-to-date).
