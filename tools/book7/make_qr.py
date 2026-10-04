"""QR code for the Book 7 companion materials folder, for the screen and print editions.

Run: python3 tools/book7/make_qr.py
Writes book7/src/figures/qr_companion.png (screen), book7/build/figures_print/qr_companion.png (greyscale, sized for
about 1.3 in at 450 ppi) and book7/publishing/qr_companion.svg (vector, for the cover or flyers), then decodes the
PNG to check that it returns the link exactly.
"""
import os
import segno
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
URL = "https://drive.google.com/drive/folders/1cLpEF8qvR_OMg0JKVFHKvLxtROvZAmfr"
qr = segno.make(URL, error="q", micro=False)
os.makedirs("book7/build/figures_print", exist_ok=True)
os.makedirs("book7/publishing", exist_ok=True)
qr.save("book7/publishing/qr_companion.svg", scale=10, border=4, dark="#000000")
mods = qr.symbol_size(scale=1, border=4)[0]
for path, px in (("book7/src/figures/qr_companion.png", 640), ("book7/build/figures_print/qr_companion.png", 585)):
    scale = max(1, px // mods)
    qr.save(path, scale=scale, border=4, dark="#000000", light="#FFFFFF")
    Image.open(path).convert("L").save(path, dpi=(450, 450))
try:
    import cv2
    for path in ("book7/src/figures/qr_companion.png", "book7/build/figures_print/qr_companion.png"):
        data, _, _ = cv2.QRCodeDetector().detectAndDecode(cv2.imread(path))
        print(path, "decodes to the link" if data == URL else f"DECODE MISMATCH: {data!r}")
except ImportError:
    print("opencv not installed: decode check skipped")
print("version", qr.version, "error correction", qr.error, "modules", mods)
