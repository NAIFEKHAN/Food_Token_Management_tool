"""PDF token generation using reportlab."""
from io import BytesIO
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from .qr_utils import data_url_to_png_bytes


GOLD = (0.83, 0.69, 0.22)
BLACK = (0, 0, 0)


def build_token_pdf(*, event_name: str, name: str, roll_no: str,
                    food_type: str, token_id: str, qr_data_url: str) -> bytes:
    """Render a single-page PDF token and return its bytes."""
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A5)
    width, height = A5

    # Black background
    c.setFillColorRGB(*BLACK)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Gold border
    c.setStrokeColorRGB(*GOLD)
    c.setLineWidth(3)
    c.rect(8 * mm, 8 * mm, width - 16 * mm, height - 16 * mm, fill=0, stroke=1)

    # Event title
    c.setFillColorRGB(*GOLD)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 25 * mm, event_name)

    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 33 * mm, "Food Token")

    # Student details
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(15 * mm, height - 55 * mm, f"Name:  {name}")
    c.drawString(15 * mm, height - 65 * mm, f"Roll No:  {roll_no}")
    c.drawString(15 * mm, height - 75 * mm, f"Food:  {food_type}")

    c.setFillColorRGB(*GOLD)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(15 * mm, height - 90 * mm, f"Token: {token_id}")

    # QR code
    qr_bytes = data_url_to_png_bytes(qr_data_url)
    qr_img = ImageReader(BytesIO(qr_bytes))
    qr_size = 55 * mm
    c.drawImage(qr_img, (width - qr_size) / 2, 18 * mm,
                width=qr_size, height=qr_size, mask='auto')

    c.setFillColorRGB(*GOLD)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width / 2, 12 * mm, "Present this token at the food counter")

    c.showPage()
    c.save()
    return buf.getvalue()
