"""
Kruti Dev (Ajay) → Unicode Devanagari transcoder.
Extracted 1:1 from degree_verification_v2_TESSERACT.ipynb (Part 1, 2, 4).
"""
import re

# Regex to identify Hindi font names in PDF character objects
HI_FONT = re.compile(r'Ajay|Kruti|Devlys|Chanakya|Kokila|Mangal', re.I)

# ── Kruti Dev → Unicode lookup table (Colab Part 2) ─────
KD: dict[str, str] = {
    'vkS': 'औ', 'vks': 'ओ', 'vk': 'आ', 'v': 'अ', 'bZ': 'ई', 'b': 'इ', 'm': 'उ', 'Å': 'ऊ', ',s': 'ऐ', ',': 'ए', '_': 'ऋ',
    'd': 'क', '[k': 'ख', 'x': 'ग', '?k': 'घ', '³': 'ङ', 'p': 'च', 'N': 'छ', 't': 'ज', '>k': 'झ', '¥': 'ञ',
    'V': 'ट', 'B': 'ठ', 'M': 'ड', '<': 'ढ', '.k': 'ण', 'r': 'त', 'Fk': 'थ', 'n': 'द', '/k': 'ध', 'u': 'न',
    'i': 'प', 'Q': 'फ', 'c': 'ब', 'Hk': 'भ', 'e': 'म', ';': 'य', 'j': 'र', 'y': 'ल', '˜': 'ळ', 'o': 'व', "'k": 'श', '"k': 'ष',
    'l': 'स', 'g': 'ह', '{k': 'क्ष', 'K': 'ज्ञ', '=': 'त्र', 'J': 'श्र',
    'ç': 'प्र', 'Ø': 'क्र', 'Ü': 'श्', 'æ': 'द्र', 'ä': 'क्त', 'Ô': 'ह्य', '#': 'रु', '$': 'रू', ')': 'द्ध', '|': 'द्य', '«': 'त्त', 'Ý': 'ङ्क', 'Þ': 'ङ्ख',
    'D': 'क्', '[': 'ख्', 'X': 'ग्', '?': 'घ्', 'P': 'च्', 'T': 'ज्', '>': 'झ्', 'U': 'न्', 'I': 'प्', 'C': 'ब्',
    'E': 'म्', 'Y': 'ल्', 'L': 'स्', 'F': 'थ्', 'H': 'भ्', '/': 'ध्', "'": 'श्', '"': 'ष्', '.': 'ण्', '{': 'क्ष्', '¸': 'य्', 'O': 'व्', 'G': 'ह्', 'R': 'त्',
    'k': 'ा', 'h': 'ी', 'q': 'ु', 'w': 'ू', 's': 'े', 'S': 'ै', 'a': 'ं', '¡': 'ँ', '%': 'ः', '~': '्', 'z': '्र', 'A': '।', 'f': 'ि', 'W': 'ृ',
    '¼': '(', '½': ')',
}

for _c in ['[k', '?k', '>k', '.k', '/k', "'k", '"k', 'Fk', 'Hk', '{k']:
    KD[_c + 's'] = KD[_c] + 'ो'
    KD[_c + 'S'] = KD[_c] + 'ौ'

_C = r'[क-हळ]़?'
_CL = rf'(?:{_C}्)*{_C}'
MAT = 'ािीुूृेैोौंँ'


def _fix_spaces(cs: list[dict]) -> list[dict]:
    """
    Fix character spacing / kerning issues from PDF extraction for Hindi chars.
    Shifts narrow non-space characters (< 1.2 width) before preceding spaces.
    """
    cs = list(cs)
    i = 0
    w = lambda c: c['x1'] - c['x0']
    while i < len(cs) - 1:
        if cs[i]['text'] == ' ' and w(cs[i + 1]) < 1.2 and cs[i + 1]['text'] != ' ':
            j = i + 1
            while j < len(cs) and w(cs[j]) < 1.2 and cs[j]['text'] != ' ':
                j += 1
            cs[i:j] = cs[i + 1:j] + [cs[i]]
            i = j
        else:
            i += 1
    return cs


def kd2uni(s: str, unmapped: set | None = None) -> str:
    """
    Convert a Kruti Dev encoded string to proper Unicode Devanagari.
    Populates `unmapped` set if provided.
    """
    s = (s or '').replace('\u00a0', ' ')
    out = []
    i = 0
    while i < len(s):
        for L in (3, 2, 1):
            ch = s[i:i + L]
            if ch in KD:
                out.append(KD[ch])
                i += L
                break
        else:
            c = s[i]
            if unmapped is not None and not c.isspace() and c not in 'Z.,-':
                unmapped.add(c)
            out.append(c)
            i += 1
    t = ''.join(out)
    t = t.replace('ाे', 'ो').replace('ाै', 'ौ')
    t = re.sub(rf'ि({_CL})', r'\1ि', t)                # short-i after its cluster
    t = re.sub(rf'({_CL})([{MAT}]*)Z', r'र्\1\2', t)   # reph before cluster
    t = t.replace('Z', 'र्')
    t = t.replace('ा्र', '्रा')                        # rakar must follow consonant, not matra
    t = t.replace('प्राद्यैो', 'प्रौद्यो')                 # known font variant
    t = t.replace('िा', 'ि')                           # extra bar glyph after wide conjunct+i
    return t