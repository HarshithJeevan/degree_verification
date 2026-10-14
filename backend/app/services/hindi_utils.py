"""
Hindi & English text normalization and comparison utilities.
Extracted 1:1 from degree_verification_v2_TESSERACT.ipynb (Part 1, 2, 3, 5).
"""
import re
import unicodedata
import difflib
from typing import Callable

from app.services.kruti_dev import kd2uni
from app.config import BAG_PASS_VOCAB, USE_OCR


# ── Normalization Helpers (Colab Part 1, 2, 3) ──────────

def norm(t: str | None) -> str:
    return re.sub(r'\s+', ' ', str(t or '').strip())


def qn(s: str | None) -> str:
    return norm(re.sub(r"[’‘“”\"']", "'", str(s or '')))


def sim(a: str | None, b: str | None) -> float:
    return round(100 * difflib.SequenceMatcher(None, str(a or ''), str(b or '')).ratio(), 1)


def hn(s: str | None) -> str:
    s = unicodedata.normalize('NFC', str(s or ''))
    s = s.replace('\u200c', '').replace('\u200d', '')
    return re.sub(r'\s+', ' ', s.strip())


def bag(s: str | None) -> str:
    """Order-insensitive glyph bag (matras split like Kruti types them)."""
    s = hn(s).replace('ो', 'ाे').replace('ौ', 'ाै').replace('\u093c', '')
    return ''.join(sorted(re.sub(r'\s+', '', s)))


def soft(s: str | None) -> str:
    """NFD normalize, strip nukta, unify chandrabindu to anusvara, strip spaces."""
    s = unicodedata.normalize('NFD', hn(s)).replace('\u093c', '').replace('ँ', 'ं')
    return re.sub(r'\s+', '', unicodedata.normalize('NFC', s))


def key(s: str | None) -> str:
    return re.sub(r'\s+', ' ', str(s or '').lower().replace('minors', 'minor')).strip()


# ── Comparison Functions (Colab Part 5) ─────────────────

def cmp_en(exp: str, found: str) -> str:
    """Exact match -> PASS, case-insensitive match -> REVIEW, else -> FAIL."""
    if exp == found:
        return 'PASS'
    return 'REVIEW' if exp.casefold() == found.casefold() else 'FAIL'


def _cmp_hi_core(exp: str, raw: str, vocab: bool = False) -> tuple[str, str, str]:
    """
    Core Hindi comparison from Colab.
    Note: If `raw` is already Unicode (e.g., from parse_page), kd2uni passes Devanagari
    chars through; to strictly check unmapped Kruti glyphs, pass raw Kruti Dev text.
    Returns: (status, converted_unicode, note)
    """
    um = set()
    # Only flag unmapped ASCII glyphs if raw isn't already Devanagari Unicode
    already_uni = any('\u0900' <= ch <= '\u097f' for ch in (raw or ''))
    conv = raw if already_uni else kd2uni(raw, um)
    e, f = hn(exp), hn(conv)
    if e == f:
        return 'PASS', conv, ''
    if um:
        return 'FAIL', conv, f'unmapped glyph(s): {sorted(um)}'
    if bag(e) == bag(f):
        return ('PASS' if vocab and BAG_PASS_VOCAB else 'REVIEW'), conv, 'same glyphs, PDF glyph order differs (font encoding variant)'
    if soft(e) == soft(f):
        return 'REVIEW', conv, 'only space/anusvara/chandrabindu/nukta differs'
    return 'FAIL', conv, f'similarity {sim(e, f)}%'


def cmp_hi_colab(
    exp: str,
    raw: str,
    vocab: bool = False,
    ocr: Callable[[], str | None] | None = None,
) -> tuple[str, str, str]:
    """
    Exact Colab signature: returns (status, conv, note).
    """
    st, conv, note = _cmp_hi_core(exp, raw, vocab)
    if st == 'FAIL' and ocr is not None and USE_OCR:
        o = ocr()
        if o is not None:
            if hn(o) == hn(exp):
                return 'REVIEW', conv, (note + ' | ' if note else '') + 'OCR matches Excel -> text-layer converter probably lacks a glyph (send me this raw text)'
            return 'FAIL', conv, (note + ' | ' if note else '') + f'OCR also differs: {hn(o)!r}'
    return st, conv, note


def cmp_hi(
    exp: str,
    raw: str,
    vocab: bool = False,
    is_vocab: bool | None = None,
    ocr: Callable[[], str | None] | str | None = None,
) -> tuple[str, float, str]:
    """
    Backend adapter wrapper around cmp_hi_colab.
    Supports both `vocab` and `is_vocab` kwargs and returns (status, similarity%, note).
    """
    use_vocab = is_vocab if is_vocab is not None else vocab
    ocr_fn = (lambda: ocr) if isinstance(ocr, str) else ocr
    st, conv, note = cmp_hi_colab(exp, raw, vocab=use_vocab, ocr=ocr_fn)
    similarity = 100.0 if st == 'PASS' else sim(hn(exp), hn(conv))
    return st, similarity, note