"""QR code generation utilities."""
import base64
from io import BytesIO
import qrcode


def generate_qr_data_url(payload: str) -> str:
    """Return a base64 PNG data URL for the given payload."""
    img = qrcode.make(payload)
    buf = BytesIO()
    img.save(buf, format="PNG")
    encoded = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def data_url_to_png_bytes(data_url: str) -> bytes:
    """Strip the data: prefix and return raw PNG bytes."""
    if "," in data_url:
        data_url = data_url.split(",", 1)[1]
    return base64.b64decode(data_url)
