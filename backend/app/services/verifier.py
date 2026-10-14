"""
Main verifier — orchestrates the full verification pipeline using the exact
verify_page() logic from degree_verification_v2_TESSERACT.ipynb (Part 5).
"""
import json
import re
from typing import Any
import pdfplumber
from sqlalchemy.orm import Session

from app.models.database import CertificateRecord
from app.services.pdf_parser import pdf_lines, parse_page, parse_degree, G, EN_FIXED, SIGN
from app.services.kruti_dev import kd2uni
from app.services.hindi_utils import norm, qn, sim, key, cmp_en, cmp_hi_colab
from app.services.ocr_service import ocr_lines
from app.services.roster import get_student_by_roll, get_vocab
from app.services.scoring import (
    map_status,
    map_field_status,
    compute_overall_confidence,
    determine_verdict,
    build_review_reason,
)
from app.config import DATE_HI, DATE_EN


def verify_page_with_db(
    page: Any,
    db: Session,
    V: dict[str, dict[str, str]],
    n_pages: int = 1,
) -> tuple[str | None, list[tuple[str, str, str, str, str]]]:
    """
    Exact Colab `verify_page` logic adapted to look up the student via SQLAlchemy `db`.
    Returns: (roll, res) where each item in `res` is (field, status, expected, found, note).
    """
    L = pdf_lines(page)
    P = parse_page(L)
    T = P['T']
    res: list[tuple[str, str, str, str, str]] = []
    add = lambda f, s, e='', fd='', n='': res.append((f, s, e, fd, n))

    m = re.search(r'Roll\s*No\.?\s*(\d{6,})', ' '.join(T))
    roll = m.group(1) if m else None

    if n_pages != 1:
        add('Pages', 'REVIEW', '1', str(n_pages))

    student = get_student_by_roll(roll, db) if roll else None
    if not student:
        add('Roll', 'FAIL', 'present in DB', roll or 'not found on PDF', 'Roll not in DB')
        return roll, res

    add('Roll', 'PASS', roll, roll)

    # Fixed Hindi & English anchors
    def fx(label: str, i: int | None, g: str):
        add(label, 'PASS' if i is not None else 'FAIL', g, L[i]['text'] if i is not None else 'MISSING')

    fx('Fixed HI: senate recommendation', P['i_sen'], G['sen'])
    fx('Fixed HI: ko', P['i_ko'], G['ko'])
    if len(DATE_HI) > 0:
        fx('Fixed HI: date line 1', P['i_d1'], DATE_HI[0])
    if len(DATE_HI) > 1:
        fx('Fixed HI: date line 2', P['i_d2'], DATE_HI[1])

    for lab, i, g in (
        ('rec', P['i_rec'], EN_FIXED[0]),
        ('confers', P['i_hc'], EN_FIXED[1]),
        ('seal', P['i_seal'], EN_FIXED[2]),
        ('date', P['i_den'], DATE_EN),
    ):
        fx('Fixed EN: ' + lab, i, g)

    for t in SIGN:
        ok = any(qn(t) in x for x in T)
        add('Signatory: ' + t, 'PASS' if ok else 'FAIL', t, 'present' if ok else 'MISSING')

    # Reconstruct full English degree string if stored split in SQLite, or use student['degree']
    expected_deg = student['degree']
    parts = parse_degree(expected_deg)
    dual = len(parts) > 1
    pg = parts[0]['prog'].startswith('Post Graduate')
    hon = any(p['hon'] for p in parts)
    minor = norm(parts[0]['minor']) if not dual and parts[0]['minor'] else ''

    # English variable part
    en = [L[i]['text'] for i in P['en_i']]
    name_en = en[0] if en else ''
    rest = en[1:]
    lead = rest[0] if rest and rest[0] in ('The', 'The Degree of') else ''
    deg_txt = norm(' '.join(rest[1:] if lead else rest))

    add('Name (EN)', cmp_en(student['name'], norm(name_en)), student['name'], norm(name_en))
    add('Degree intro (EN)', 'PASS' if lead == ('The' if pg else 'The Degree of') else 'FAIL', 'The' if pg else 'The Degree of', lead or 'MISSING')
    add('Degree (EN)', cmp_en(expected_deg, deg_txt), expected_deg, deg_txt)

    # Hindi name
    nraw = ' '.join(L[i]['text'] for i in P['name_hi_i'])
    st, cv, nt = cmp_hi_colab(
        student['name_hi'],
        nraw,
        ocr=lambda: ocr_lines(page, [L[i] for i in P['name_hi_i']]),
    )
    add('Name (HI)', st, student['name_hi'], cv, (nt + ' ' if nt else '') + f'raw={nraw!r}')

    # Hindi degree block
    block = [L[i] for i in P['block_i']]
    seps = [qn(l['text']) for l in block if qn(l['text']) in (G['men'], G['and_'])]
    content = [l['text'] for l in block if qn(l['text']) not in (G['men'], G['and_'])]
    content_l = [l for l in block if qn(l['text']) not in (G['men'], G['and_'])]

    def ref(p: dict) -> tuple[str | None, str | None]:
        d = V.get('disc', {}).get(key(p['disc'])) if p['disc'] else None
        g = V.get('prog', {}).get(key(re.sub(r'^Three\s*-\s*Year\s+', '', p['prog'])))
        return d, g

    if hon or (dual and (parts[0]['minor'] or parts[1]['minor'])):
        add('Degree block (HI)', 'REVIEW', '(honours / dual+minor layout not yet templated)', ' | '.join(kd2uni(x) for x in content), 'send a sample certificate of this type')
    elif dual:
        add('Fixed HI: and (,oa)', 'PASS' if seps == [G['and_']] else 'FAIL', G['and_'], str(seps))
        for k, p in enumerate(parts):
            d, g = ref(p)
            lab = f'Degree line (HI) {k + 1}'
            if k >= len(content):
                add(lab, 'FAIL', 'line present', 'MISSING')
                continue
            if d and g:
                st, cv, nt = cmp_hi_colab(f'{d} में {g}', content[k], vocab=True, ocr=lambda k=k: ocr_lines(page, [content_l[k]]))
                add(lab, st, f'{d} में {g}', cv, nt)
            else:
                add(lab, 'REVIEW', 'no Hindi reference in sheet for ' + str(p['disc'] or p['prog']), kd2uni(content[k]))
    else:
        add('Fixed HI: men (esa)', 'PASS' if seps == [G['men']] else 'FAIL', G['men'], str(seps))
        d, g = ref(parts[0])
        if len(content) != 2:
            add('Discipline (HI)', 'FAIL', '2 lines (discipline, degree type)', f'{len(content)} lines')
        else:
            for lab, e, raw, what, li in (
                ('Discipline (HI)', d, content[0], parts[0]['disc'], 0),
                ('Degree type (HI)', g, content[1], parts[0]['prog'], 1),
            ):
                if e:
                    st, cv, nt = cmp_hi_colab(e, raw, vocab=True, ocr=lambda li=li: ocr_lines(page, [content_l[li]]))
                    add(lab, st, e, cv, nt)
                else:
                    add(lab, 'REVIEW', 'no Hindi reference in sheet for ' + str(what), kd2uni(raw))

    # Hindi confers line
    ci = P['i_conf']
    craw = L[ci]['text'] if ci is not None else None
    if craw is None:
        add('Hindi confers line', 'FAIL', 'present', 'MISSING')
    elif minor and not hon and not dual:
        mh = V.get('minor', {}).get(key(minor))
        if mh:
            st, cv, nt = cmp_hi_colab(f'की उपाधि {mh} प्रदान करता है', craw, vocab=True, ocr=lambda: ocr_lines(page, [L[ci]]))
            add('Hindi confers line (minor)', st, f'की उपाधि {mh} प्रदान करता है', cv, nt)
        else:
            add('Hindi confers line (minor)', 'REVIEW', 'no Hindi reference for ' + minor, kd2uni(craw))
    elif hon or (dual and parts[0]['minor']):
        add('Hindi confers line', 'REVIEW', '(not yet templated)', kd2uni(craw))
    else:
        g = G['pg'] if pg else G['plain']
        add('Hindi confers line', 'PASS' if qn(craw) == qn(g) else 'FAIL', g, craw)

    used = set(P['name_hi_i'] + P['block_i'] + P['en_i']) | {
        P[k] for k in ('i_sen', 'i_ko', 'i_conf', 'i_d1', 'i_d2', 'i_rec', 'i_hc', 'i_seal', 'i_den') if P[k] is not None
    }
    used |= {i for i, t in enumerate(T) if 'Roll No' in t or any(qn(x) in t for x in SIGN)}
    un = [L[i]['text'] for i in range(len(L)) if i not in used]
    add('Unexpected lines', 'PASS' if not un else 'REVIEW', 'none', '; '.join(un))

    return roll, res


def run_verification(cert_id: str, file_path: str, db: Session) -> str:
    """
    Run the full Colab verification pipeline on a certificate and update SQLite.
    """
    cert = db.query(CertificateRecord).filter(CertificateRecord.id == cert_id).first()
    if not cert:
        return "pending"

    field_results: list[dict] = []
    V = get_vocab(db)

    try:
        with pdfplumber.open(file_path) as doc:
            roll, res = verify_page_with_db(doc.pages[0], db, V, n_pages=len(doc.pages))
            if roll:
                cert.roll_number = roll
            for f, s, e, fd, note in res:
                field_results.append({
                    "field": f,
                    "status": s,
                    "expected": e,
                    "found": fd,
                    "similarity": 100.0 if s == "PASS" else sim(e, fd),
                    "note": note,
                })
    except Exception as e:
        field_results.append({
            "field": "PDF Processing",
            "status": "FAIL",
            "expected": "—",
            "found": str(e),
            "similarity": 0.0,
            "note": f"Error processing PDF: {e}",
        })

    verdict = determine_verdict(field_results)
    frontend_status = map_status(verdict)
    confidence = compute_overall_confidence(field_results)
    review_reason = build_review_reason(field_results)

    frontend_fields = []
    for f in field_results:
        frontend_fields.append({
            "name":           f.get("field"),
            "expectedValue":  f.get("expected"),
            "extractedValue": f.get("found"),
            "matchStatus":    map_field_status(f.get("status", "REVIEW")),
            "confidence":     f.get("similarity", 0.0),
            "matchType":      "exact" if f.get("status") == "PASS" else "fuzzy",
            "reason":         f.get("note"),
        })

    cert.status              = frontend_status
    cert.overall_confidence  = confidence
    cert.review_reason       = review_reason
    cert.verification_result = json.dumps({"fields": frontend_fields})
    db.commit()

    return frontend_status