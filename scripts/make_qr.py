"""Make QR codes for sharing the dashboards (PNG for slides/print, SVG for posters).
Run: python scripts/make_qr.py   (needs: pip install "qrcode[pil]")
High error correction (H): the code still scans when printed small, slightly damaged or partly covered."""
from pathlib import Path

import qrcode
import qrcode.image.svg

ROOT = Path(__file__).resolve().parents[1]
APPS = {
    "respiratory_watch": "https://episurveil-respiratory.streamlit.app/",
    "episurveil": "https://episurveil.streamlit.app/",
}


def make(name: str, url: str, out: Path) -> None:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=16, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    qr.make_image(fill_color="#1F2328", back_color="white").save(out / f"qr_{name}.png")
    qr.make_image(image_factory=qrcode.image.svg.SvgPathImage).save(out / f"qr_{name}.svg")


if __name__ == "__main__":
    out = ROOT / "app" / "assets"
    out.mkdir(parents=True, exist_ok=True)
    for name, url in APPS.items():
        make(name, url, out)
        print("written", out / f"qr_{name}.png", "and .svg ->", url)
