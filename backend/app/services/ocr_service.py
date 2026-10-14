"""
Tesseract OCR fallback service.
Extracted 1:1 from degree_verification_v2_TESSERACT.ipynb (Part 5).
"""
import pytesseract
from typing import Any

from app.config import TESSERACT_CMD

if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def ocr_lines(page: Any, lns: list[dict | tuple], tessdata_dir: str | None = None) -> str | None:
    """
    OCR the given line dicts or bounding-box tuples with Tesseract (Hindi).
    Returns a single space-joined string (exact Colab behavior), or None if unavailable.
    """
    try:
        cfg = '--psm 7' + (f' --tessdata-dir {tessdata_dir}' if tessdata_dir else '')
        out = []
        for ln in lns:
            if isinstance(ln, dict):
                x0, top, x1, bottom = ln['x0'], ln['top'], ln['x1'], ln['bottom']
            else:
                x0, top, x1, bottom = ln[0], ln[1], ln[2], ln[3]
            box = (
                max(0, x0 - 6),
                max(0, top - 6),
                min(page.width, x1 + 6),
                min(page.height, bottom + 6),
            )
            img = page.crop(box).to_image(resolution=300).original
            out.append(' '.join(pytesseract.image_to_string(img, lang='hin', config=cfg).split()))
        return ' '.join(out)
    except Exception:
        return None