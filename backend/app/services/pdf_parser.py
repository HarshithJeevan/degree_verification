"""
PDF text-layer parser — extracts lines and identifies template fields.
Extracted 1:1 from degree_verification_v2_TESSERACT.ipynb (Part 3, 4, 5, 7).
"""
import collections
import re
from typing import Any

from app.services.kruti_dev import HI_FONT, _fix_spaces, kd2uni
from app.services.hindi_utils import norm, qn
from app.config import COLUMN_GAP, SPACE_GAP, DATE_HI, DATE_EN

# ── Fixed Template Anchors (Colab Part 5) ───────────────
G = dict(
    sen="vfHk\"kn~ dh vuq'kalk ij",
    ko='dks',
    men='esa',
    and_=',oa',
    plain='dh mikf/k iznku djrk gS',
    pg='iznku djrk gS',
)
EN_FIXED = [
    'On the recommendation of the Senate',
    'hereby confers on',
    'Given under the seal of the Institute',
]
SIGN = [
    "v/;{k] vfHk'kn~",
    'dqylfpo',
    "v/;{k] 'kklh e.My",
    'Chairman, Senate',
    'Registrar',
    'Chairman, Board of Governors',
]

DEG_RE = re.compile(
    r'^(?P<prog>(?:Three\s*-\s*Year\s+)?(?:Bachelor of \w+|Master of \w+|Executive Masters|Doctor of Philosophy|Post Graduate Diploma of the Institute))'
    r'(?P<hon>\s+with Honours)?'
    r'(?:\s+in\s+(?P<disc>.+?))?'
    r'(?P<minor>\s+with Minors?\s+in\s+.+)?$'
)


def parse_degree(d: str) -> list[dict]:
    """Split single/dual English degree strings into structured parts (Colab Part 3)."""
    parts = re.split(r'\s+and\s+(?=(?:Bachelor|Master|Executive|Doctor|Post Graduate)\b)', norm(d))
    out = []
    for p in parts:
        m = DEG_RE.match(p)
        out.append(m.groupdict() if m else dict(prog=p, hon=None, disc=None, minor=None))
    return out


def pdf_lines(page: Any) -> list[dict]:
    """
    Parse character objects from a pdfplumber page, group into lines (Colab Part 4).
    Preserves content-stream order for Hindi; sorts by x0 for English.
    """
    rows = []
    for c in page.chars:  # content-stream order kept
        ym = (c['top'] + c['bottom']) / 2
        for r in rows:
            if abs(ym - r['y']) <= max(3.0, 0.4 * c['size']):
                r['c'].append(c)
                break
        else:
            rows.append({'y': ym, 'c': [c]})

    lines = []
    for r in sorted(rows, key=lambda r: r['y']):
        xs = sorted(r['c'], key=lambda c: c['x0'])
        cuts = []
        for p, c in zip(xs, xs[1:]):
            if c['x0'] - p['x1'] > COLUMN_GAP * max(p['size'], c['size']):
                cuts.append((p['x1'] + c['x0']) / 2)

        segs = collections.defaultdict(list)
        for c in r['c']:
            segs[sum(c['x0'] > t for t in cuts)].append(c)

        for k in sorted(segs):
            sg = segs[k]
            hindi = any(HI_FONT.search(c['fontname']) for c in sg)
            if hindi:
                txt = ''.join(c['text'] for c in _fix_spaces(sg))
            else:
                sx = sorted(sg, key=lambda c: c['x0'])
                txt = ''
                for j, c in enumerate(sx):
                    if j and c['text'] != ' ' and not txt.endswith(' ') and c['x0'] - sx[j - 1]['x1'] > SPACE_GAP * c['size']:
                        txt += ' '
                    txt += c['text']
            txt = norm(txt)
            if txt:
                x0 = min(c['x0'] for c in sg)
                x1 = max(c['x1'] for c in sg)
                top = min(c['top'] for c in sg)
                bottom = max(c['bottom'] for c in sg)
                fonts = sorted({c['fontname'].split('+')[-1] for c in sg})
                lines.append(dict(
                    text=txt,
                    hindi=hindi,
                    is_hindi=hindi,
                    x0=x0,
                    x1=x1,
                    top=top,
                    bottom=bottom,
                    y=top,
                    bbox=(x0, top, x1, bottom),
                    fonts=fonts,
                    font=fonts[0] if fonts else '',
                ))
    return lines


def parse_page(L: list[dict]) -> dict:
    """
    Identify fixed anchor indices and extract variable slots (Colab Part 5 & 7).
    Returns both the exact Colab index keys (`i_sen`, `name_hi_i`, etc.) AND
    pre-extracted convenience keys (`roll_number`, `name_en`, `name_hi`, etc.).
    """
    T = [qn(l['text']) for l in L]

    def idx(g: str, s: int = 0) -> int | None:
        return next((i for i in range(s, len(T)) if T[i] == qn(g)), None)

    P: dict[str, Any] = dict(i_sen=idx(G['sen']))
    P['i_ko'] = idx(G['ko'], P['i_sen'] or 0)
    P['i_d1'] = idx(DATE_HI[0]) if len(DATE_HI) > 0 else None
    P['i_d2'] = idx(DATE_HI[1]) if len(DATE_HI) > 1 else None
    P['i_conf'] = P['i_d1'] - 1 if P['i_d1'] else None
    P['i_rec'] = idx(EN_FIXED[0])
    P['i_hc'] = idx(EN_FIXED[1])
    P['i_seal'] = idx(EN_FIXED[2])
    P['i_den'] = idx(DATE_EN, P['i_seal'] or 0)

    g = lambda a, b: [i for i in range(a + 1, b)] if a is not None and b is not None and b > a else []
    P['name_hi_i'] = g(P['i_sen'], P['i_ko'])
    P['block_i'] = g(P['i_ko'], P['i_conf'])
    P['en_i'] = g(P['i_hc'], P['i_seal'])
    P['T'] = T

    # Also populate extracted fields for compatibility
    m = re.search(r'Roll\s*No\.?\s*(\d{6,})', ' '.join(T))
    P['roll_number'] = m.group(1) if m else None

    en = [L[i]['text'] for i in P['en_i']]
    name_en = norm(en[0]) if en else ''
    rest = en[1:]
    lead = rest[0] if rest and rest[0] in ('The', 'The Degree of') else ''
    deg_txt = norm(' '.join(rest[1:] if lead else rest))
    parts = parse_degree(deg_txt) if deg_txt else []

    name_hi_raw = ' '.join(L[i]['text'] for i in P['name_hi_i'])
    P['name_en'] = name_en
    P['intro_en'] = lead
    P['degree_en'] = deg_txt
    P['branch_en'] = ' | '.join(norm(p['disc'] or '') for p in parts if p.get('disc'))
    P['name_hi_raw'] = name_hi_raw
    P['name_hi'] = kd2uni(name_hi_raw)
    P['degree_hi'] = ' | '.join(kd2uni(L[i]['text']) for i in P['block_i'] if qn(L[i]['text']) not in (G['men'], G['and_']))
    P['confers_hi'] = L[P['i_conf']]['text'] if P['i_conf'] is not None else None

    return P