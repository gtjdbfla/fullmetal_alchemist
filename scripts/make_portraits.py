"""Generate ID-photo style SVG portraits for the public characters page.

Output: site/portraits/<slug>.svg
Run:    python scripts/make_portraits.py
The slug/appearance table at the bottom is also written into
private/dashboard-config.json (publicCharacters[].portrait / appearance).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "portraits"
CONFIG = ROOT / "private" / "dashboard-config.json"


# ---------- colour helpers ----------
def _rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a: str, b: str, t: float) -> str:
    ra, rb = _rgb(a), _rgb(b)
    return "#%02x%02x%02x" % tuple(round(ra[i] + (rb[i] - ra[i]) * t) for i in range(3))


def dark(c, t=0.25):
    return mix(c, "#000000", t)


def light(c, t=0.25):
    return mix(c, "#ffffff", t)


# ---------- face ----------
FACE = {
    "round": "M72 118 C72 82 94 64 120 64 C146 64 168 82 168 118 C168 154 152 190 120 197 C88 190 72 154 72 118 Z",
    "strong": "M71 116 C71 80 94 64 120 64 C146 64 169 80 169 116 L165 158 C161 182 142 197 120 199 C98 197 79 182 75 158 Z",
    "narrow": "M74 118 C74 82 95 64 120 64 C145 64 166 82 166 118 C166 156 148 192 120 202 C92 192 74 156 74 118 Z",
    "soft": "M70 120 C70 82 94 66 120 66 C146 66 170 82 170 120 C170 158 152 192 120 196 C88 192 70 158 70 120 Z",
}

# ---------- hair: (back, front, over) ----------
def hair(style: str, h: str):
    hs = dark(h, 0.22)
    hl = light(h, 0.18)
    back = front = over = ""
    f = lambda d, c=h, extra="": f'<path d="{d}" fill="{c}" {extra}/>'
    if style == "swept":
        front = f("M69 116 C63 72 90 48 122 48 C154 48 178 70 171 116 C167 100 161 88 150 82 C140 94 118 90 100 80 C92 92 78 102 69 116 Z")
        front += f"<path d='M96 62 C110 54 130 54 146 62' stroke='{hl}' stroke-width='3' fill='none' opacity='.5' stroke-linecap='round'/>"
    elif style == "neat":
        front = f("M69 116 C63 72 90 46 120 46 C152 46 178 70 171 116 C167 98 160 84 148 78 C132 70 104 72 90 80 C80 90 74 100 69 116 Z")
        front += f"<path d='M104 74 C100 62 104 52 112 48' stroke='{hs}' stroke-width='2' fill='none'/>"
    elif style == "spiky":
        front = f("M69 116 C64 74 88 50 118 46 L126 32 L134 48 L150 38 L152 56 C172 66 174 92 171 116 C165 96 158 86 148 82 L140 88 L128 80 L116 88 L104 80 L92 86 C82 94 74 104 69 116 Z")
    elif style == "cowlick":
        back = f("M67 120 C62 70 92 46 122 46 C152 46 182 70 173 120 L170 172 L70 172 Z")
        front = f("M69 116 C62 68 92 46 122 46 C154 46 180 70 171 116 C168 100 162 88 154 82 C148 96 140 100 134 84 C128 98 116 100 110 84 C104 96 96 98 92 86 C82 94 74 104 69 116 Z")
        front += f("M70 100 C62 128 64 160 72 184 C80 162 80 128 84 102 Z", hs)
        front += f("M170 100 C178 128 176 160 168 184 C160 162 160 128 156 102 Z", hs)
        front += f"<path d='M118 50 C110 34 120 22 132 30' stroke='{h}' stroke-width='5' fill='none' stroke-linecap='round'/>"
        front += f"<path d='M100 62 C112 54 134 54 146 62' stroke='{hl}' stroke-width='3' fill='none' opacity='.55' stroke-linecap='round'/>"
        # braid over the right shoulder
        segs = "".join(f"<ellipse cx='{162 + i * 1.8:.1f}' cy='{208 + i * 17}' rx='9' ry='11' fill='{h if i % 2 == 0 else hs}' transform='rotate({-8 + i * 3} {162 + i * 1.8:.1f} {208 + i * 17})'/>" for i in range(5))
        over = segs + f"<rect x='158' y='292' width='12' height='8' rx='3' fill='#b83a2f'/>"
    elif style == "soft":
        back = f("M68 122 C60 70 92 46 120 46 C150 46 182 70 172 122 L170 168 L70 168 Z", hs)
        front = f("M69 120 C62 72 90 50 120 50 C150 50 178 72 171 120 C166 100 158 90 146 84 C138 96 128 92 120 80 C112 92 102 96 94 84 C82 90 74 102 69 120 Z")
        front += f("M70 104 C64 130 66 156 74 172 C80 152 80 128 84 106 Z", hs)
        front += f("M170 104 C176 130 174 156 166 172 C160 152 160 128 156 106 Z", hs)
    elif style == "updo":
        back = f("<")[:0]
        back = f"<ellipse cx='120' cy='48' rx='30' ry='16' fill='{h}'/><ellipse cx='120' cy='44' rx='20' ry='10' fill='{hl}' opacity='.35'/>"
        front = f("M70 116 C64 74 90 52 120 52 C150 52 176 74 170 116 C166 102 160 92 148 88 C132 98 108 90 94 80 C86 92 78 104 70 116 Z")
        front += f"<path d='M150 86 C158 104 160 128 156 150' stroke='{h}' stroke-width='6' fill='none' stroke-linecap='round'/>"
        front += "<rect x='136' y='54' width='22' height='7' rx='3' fill='#c8a24a' transform='rotate(18 147 57)'/>"
    elif style == "topknot":
        back = f"<circle cx='120' cy='40' r='16' fill='{h}'/>"
        front = f("M72 112 C66 74 92 54 120 54 C148 54 174 74 168 112 C160 94 142 82 120 82 C98 82 80 94 72 112 Z")
        front += f("M76 104 C72 128 74 154 82 176 C86 152 84 126 86 106 Z", hs)
        front += f("M164 104 C168 128 166 154 158 176 C154 152 156 126 154 106 Z", hs)
        front += "<path d='M100 54 L104 38 L112 46 L120 32 L128 46 L136 38 L140 54 Z' fill='#d6a935' stroke='#9a7418' stroke-width='1.5' stroke-linejoin='round'/>"
    elif style == "bun":
        back = f"<circle cx='80' cy='56' r='18' fill='{h}'/><circle cx='160' cy='56' r='18' fill='{h}'/>"
        back += f"<circle cx='80' cy='56' r='18' fill='none' stroke='{hl}' stroke-width='2' opacity='.35'/><circle cx='160' cy='56' r='18' fill='none' stroke='{hl}' stroke-width='2' opacity='.35'/>"
        front = f("M72 114 C68 74 92 54 120 54 C148 54 172 74 168 114 C150 98 90 98 72 114 Z")
        front += f("M72 100 C66 126 68 152 74 168 C80 148 80 124 84 104 Z", hs)
        front += f("M168 100 C174 126 172 152 166 168 C160 148 160 124 156 104 Z", hs)
        front += "<rect x='70' y='58' width='20' height='6' rx='3' fill='#d6a935' transform='rotate(-20 80 61)'/><rect x='150' y='58' width='20' height='6' rx='3' fill='#d6a935' transform='rotate(20 160 61)'/>"
    elif style == "bob":
        back = f("M64 116 C60 62 92 42 120 42 C150 42 182 62 176 116 L178 176 C176 184 166 186 158 180 L82 180 C74 186 64 184 62 176 Z", hs)
        front = f("M72 114 C68 74 92 56 120 56 C148 56 172 74 168 114 L168 100 C150 94 90 94 72 100 Z")
    elif style == "longtied":
        back = f("M67 124 C62 68 92 46 120 46 C148 46 178 68 173 124 L168 176 C150 186 90 186 72 176 Z", hs)
        front = f("M70 114 C64 72 92 50 120 50 C150 50 178 72 170 114 C164 96 148 84 128 80 L120 78 L112 80 C92 84 76 96 70 114 Z")
        front += f("M70 104 C64 130 66 150 72 164 C78 146 78 126 82 106 Z", hs)
        front += f("M170 104 C176 130 174 150 168 164 C162 146 162 126 158 106 Z", hs)
    elif style == "balding":
        front = f("M78 100 C82 76 100 66 120 66 C140 66 158 76 162 100 C150 84 138 78 120 78 C102 78 90 84 78 100 Z")
        front += f("M71 104 C66 122 68 140 73 148 L77 120 Z", h)
        front += f("M169 104 C174 122 172 140 167 148 L163 120 Z", h)
    elif style == "buzz":
        front = f("M71 114 C68 76 94 58 120 58 C146 58 172 76 169 114 C164 100 150 92 120 92 C90 92 76 100 71 114 Z")
    elif style == "elder":
        back = f("M70 120 C66 78 94 56 120 56 C148 56 174 78 170 120 L166 150 L74 150 Z", h)
        front = f("M71 112 C68 78 94 62 120 62 C146 62 172 78 169 112 C160 96 146 88 120 88 C94 88 80 96 71 112 Z")
    elif style == "mop":
        front = f("M68 118 C60 72 88 46 120 46 C154 46 180 72 172 118 C170 100 164 88 156 86 L150 98 L142 84 L130 96 L120 82 L110 96 L100 84 L90 98 L84 86 C76 92 70 104 68 118 Z")
    elif style == "curly":
        cs = [(84, 76), (100, 62), (120, 58), (140, 62), (156, 76), (78, 96), (162, 96), (110, 74), (132, 74)]
        front = "".join(f"<circle cx='{x}' cy='{y}' r='15' fill='{h}'/>" for x, y in cs)
    elif style == "slick":
        back = f("M68 120 C62 70 92 44 120 44 C150 44 180 70 172 120 L176 190 L64 190 Z", hs)
        front = f("M70 114 C66 74 92 52 120 52 C148 52 174 74 170 114 C160 92 140 78 120 78 C100 78 80 92 70 114 Z")
        front += f"<path d='M96 64 C112 56 134 56 150 66' stroke='{hl}' stroke-width='3' fill='none' opacity='.5' stroke-linecap='round'/>"
    return back, front, over


def turban(c: str):
    cs = dark(c, 0.18)
    s = f'<path d="M64 106 C64 58 96 40 120 40 C150 40 176 58 176 106 C158 92 142 88 120 88 C98 88 82 92 64 106 Z" fill="{c}"/>'
    s += f'<path d="M72 90 C100 68 140 66 170 86 M70 102 C100 82 142 80 172 100 M84 66 C110 54 140 56 160 66" stroke="{cs}" stroke-width="3" fill="none"/>'
    return s


def headwrap(c: str):
    cs = dark(c, 0.2)
    s = f'<path d="M62 110 C60 60 94 40 120 40 C148 40 180 60 178 110 C160 94 142 90 120 90 C98 90 80 94 62 110 Z" fill="{c}"/>'
    s += f'<path d="M62 110 C56 144 60 182 76 206 L94 198 C80 178 78 148 80 104 Z" fill="{cs}"/>'
    s += f'<path d="M70 84 C100 68 142 68 172 84 M66 98 C100 84 144 84 176 98" stroke="{cs}" stroke-width="3" fill="none"/>'
    return s


# ---------- clothing ----------
def clothing(kind: str, c: dict, x: dict):
    base = c["cloth"]
    sh = "M14 300 C14 262 52 242 102 234 L138 234 C188 242 226 262 226 300 Z"
    s = f'<path d="{sh}" fill="{base}"/>'
    s += f'<path d="M30 300 C34 270 62 252 102 244 L138 244" stroke="{light(base, .12)}" stroke-width="3" fill="none" opacity=".6"/>'
    if kind == "uniform":
        s += f'<path d="M104 232 L120 266 L136 232 Z" fill="#f2f0ea"/>'
        s += f'<path d="M92 226 L106 230 L112 262 L88 266 Z" fill="{light(base, .08)}" stroke="#c9a640" stroke-width="1.4"/>'
        s += f'<path d="M148 226 L134 230 L128 262 L152 266 Z" fill="{light(base, .08)}" stroke="#c9a640" stroke-width="1.4"/>'
        for y in (276, 290):
            s += f'<circle cx="120" cy="{y}" r="3.2" fill="#d6b24a"/>'
        pips = x.get("pips", 0)
        for i in range(pips):
            s += f'<path d="M{97 + i * 8} 240 l2.2 4.4 4.8 .7 -3.5 3.4 .8 4.8 -4.3 -2.3 -4.3 2.3 .8 -4.8 -3.5 -3.4 4.8 -.7z" fill="#e2c05a"/>'
        if x.get("stripe"):
            s += '<rect x="30" y="268" width="26" height="4" fill="#c9a640" transform="rotate(-18 43 270)"/><rect x="184" y="268" width="26" height="4" fill="#c9a640" transform="rotate(18 197 270)"/>'
    elif kind == "suit":
        s += f'<path d="M104 232 L120 272 L136 232 Z" fill="#f4f2ec"/>'
        s += f'<path d="M104 232 L82 262 L98 296 L116 262 Z" fill="{light(base, .1)}"/>'
        s += f'<path d="M136 232 L158 262 L142 296 L124 262 Z" fill="{light(base, .1)}"/>'
        s += f'<path d="M116 244 L124 244 L127 278 L120 288 L113 278 Z" fill="{x.get("tie", "#7a2c32")}"/>'
    elif kind == "jacket":
        s += f'<path d="M104 232 L120 262 L136 232 Z" fill="#efece4"/>'
        s += f'<path d="M96 228 L108 232 L116 268 L90 270 Z" fill="{light(base, .08)}"/><path d="M144 228 L132 232 L124 268 L150 270 Z" fill="{light(base, .08)}"/>'
        if x.get("scarf"):
            s += f'<path d="M96 232 C108 250 132 250 144 232 L148 246 C132 262 108 262 92 246 Z" fill="{x["scarf"]}"/>'
    elif kind == "sweater":
        s += f'<ellipse cx="120" cy="238" rx="25" ry="12" fill="{dark(base, .2)}"/>'
        s += f'<path d="M96 240 C106 252 134 252 144 240" stroke="{light(base, .25)}" stroke-width="4" fill="none"/>'
    elif kind == "imperial":
        s += f'<path d="M14 300 C14 262 52 242 102 234" stroke="#d6a935" stroke-width="4" fill="none"/><path d="M226 300 C226 262 188 242 138 234" stroke="#d6a935" stroke-width="4" fill="none"/>'
        s += f'<path d="M92 226 L106 230 L112 258 L90 262 Z" fill="#d6a935"/><path d="M148 226 L134 230 L128 258 L150 262 Z" fill="#d6a935"/>'
        s += '<circle cx="120" cy="276" r="12" fill="#d6a935"/><circle cx="120" cy="276" r="7" fill="none" stroke="#7a5a12" stroke-width="2"/>'
    elif kind == "tunic":
        trim = x.get("trim", "#d6a935")
        s += f'<path d="M92 226 L106 230 L112 258 L90 262 Z" fill="{trim}"/><path d="M148 226 L134 230 L128 258 L150 262 Z" fill="{trim}"/>'
        s += f'<path d="M120 258 L120 300" stroke="{trim}" stroke-width="3"/>'
        s += "".join(f'<circle cx="{xx}" cy="{yy}" r="2.6" fill="{trim}"/>' for xx, yy in ((120, 272), (120, 286)))
    elif kind == "wrap":
        s += f'<path d="M100 232 L120 262 L140 232 Z" fill="{dark(base, .35)}"/>'
        s += f'<path d="M100 232 L160 300 L128 300 L96 252 Z" fill="{light(base, .1)}"/><path d="M140 232 L80 300 L112 300 L144 252 Z" fill="{dark(base, .08)}"/>'
        s += f'<path d="M84 280 L156 252" stroke="{dark(base, .25)}" stroke-width="3" opacity=".6"/>'
    elif kind == "worker":
        s += f'<path d="M98 234 C108 252 132 252 142 234" fill="{dark(base, .3)}"/>'
        s += f'<path d="M98 234 C108 252 132 252 142 234" stroke="{dark(base, .15)}" stroke-width="3" fill="none"/>'
        s += f'<path d="M120 252 L120 300" stroke="{dark(base, .2)}" stroke-width="2" opacity=".6"/>'
    elif kind == "vest":
        s += f'<path d="M104 232 L120 262 L136 232 Z" fill="#efe6d2"/>'
        s += f'<path d="M104 232 L86 262 L96 300 L120 300 L120 262 Z" fill="{x.get("vest", "#2d6a68")}"/><path d="M136 232 L154 262 L144 300 L120 300 L120 262 Z" fill="{x.get("vest", "#2d6a68")}"/>'
    elif kind == "coat":
        s += f'<path d="M104 232 L120 266 L136 232 Z" fill="#d9d2bf"/>'
        s += f'<path d="M86 226 L106 230 L116 270 L84 280 Z" fill="{light(base, .1)}"/><path d="M154 226 L134 230 L124 270 L156 280 Z" fill="{light(base, .1)}"/>'
        if x.get("scarf"):
            s += f'<path d="M92 232 C108 254 132 254 148 232 L150 248 C134 266 106 266 90 248 Z" fill="{x["scarf"]}"/>'
    elif kind == "robe":
        s += f'<path d="M100 232 L120 268 L140 232 Z" fill="{dark(base, .3)}"/>'
        s += f'<path d="M100 232 L120 268 L140 232" stroke="{x.get("trim", "#3b5a8a")}" stroke-width="7" fill="none" stroke-linejoin="round"/>'
        s += f'<path d="M120 268 L120 300" stroke="{x.get("trim", "#3b5a8a")}" stroke-width="5"/>'
    elif kind == "masked":
        s += f'<path d="M96 226 C104 244 136 244 144 226 L150 250 C136 262 104 262 90 250 Z" fill="#12141a"/>'
        s += '<path d="M92 236 C104 252 136 252 148 236" stroke="#3a3f4a" stroke-width="2" fill="none"/>'
    return s


# ---------- face features ----------
def eyes(shape: str, iris: str, ink: str):
    P = {
        "normal": dict(w=11, top=10, bot=7, o=0, i=0),
        "sharp": dict(w=11.5, top=8.5, bot=5.5, o=-3.5, i=1.5),
        "fox": dict(w=12, top=5.5, bot=4, o=-3, i=1),
        "round": dict(w=10, top=12, bot=9, o=1, i=0),
        "soft": dict(w=10.5, top=9.5, bot=7.5, o=2, i=-0.5),
        "heavy": dict(w=11, top=7, bot=6, o=1, i=0),
    }[shape]
    out = ""
    for side, cx in ((-1, 99), (1, 141)):
        cy = 130
        w = P["w"]
        ox, ix = cx + side * w, cx - side * w
        oy, iy = cy + P["o"], cy + P["i"]
        eye = f"M{ox} {oy} Q{cx} {cy - P['top'] * 1.5} {ix} {iy} Q{cx} {cy + P['bot'] * 1.6} {ox} {oy} Z"
        cid = f"e{cx}"
        out += f'<clipPath id="{cid}"><path d="{eye}"/></clipPath>'
        out += f'<path d="{eye}" fill="#fbfaf6"/>'
        r = min(P["top"], 8.4) * 0.78
        out += f'<g clip-path="url(#{cid})"><circle cx="{cx}" cy="{cy}" r="{r + 0.8:.1f}" fill="{iris}"/><circle cx="{cx}" cy="{cy}" r="{r * 0.52:.1f}" fill="{dark(iris, .75)}"/><circle cx="{cx - 2}" cy="{cy - 2.4}" r="1.7" fill="#fff" opacity=".85"/><path d="{eye}" fill="none" stroke="{dark(iris, .6)}" stroke-width="2.4" opacity=".18"/></g>'
        out += f'<path d="M{ox} {oy} Q{cx} {cy - P["top"] * 1.5} {ix} {iy}" stroke="{ink}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
        out += f'<path d="M{ox} {oy} Q{cx} {cy + P["bot"] * 1.6} {ix} {iy}" stroke="{ink}" stroke-width="1" fill="none" opacity=".45"/>'
    return out


def brows(c: str, thick=3.2, angle=0, arch=0, y=112):
    out = ""
    for side in (-1, 1):
        xo, xi = 120 + side * 36, 120 + side * 9
        yo, yi = y - 1 - arch * 0.3, y + angle
        out += f'<path d="M{xo} {yo} Q{120 + side * 22} {y - 5 - arch} {xi} {yi}" stroke="{c}" stroke-width="{thick}" fill="none" stroke-linecap="round"/>'
    return out


def mouth(kind: str, skin: str):
    lip = mix(skin, "#8a3a3a", 0.45)
    if kind == "smile":
        return f'<path d="M105 172 Q120 184 135 172" stroke="{lip}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
    if kind == "smirk":
        return f'<path d="M106 175 Q120 176 136 169" stroke="{lip}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
    if kind == "frown":
        return f'<path d="M107 177 Q120 170 133 177" stroke="{lip}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
    if kind == "soft":
        return f'<path d="M108 173 Q120 179 132 173" stroke="{lip}" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
    return f'<path d="M107 174 Q120 176 133 174" stroke="{lip}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'


def make(spec: dict) -> str:
    skin = spec["skin"]
    sk_d = dark(skin, 0.14)
    ink = spec.get("ink", dark(spec["hair"], 0.55) if spec.get("hair") else "#2a2420")
    hair_col = spec.get("hair", "#222")
    bg = spec["bg"]
    jaw = spec.get("jaw", "round")
    back, front, over = hair(spec["style"], hair_col) if spec.get("style") else ("", "", "")
    b = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 300" width="240" height="300" role="img" aria-label="{spec["name"]}">']
    b.append(f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{light(bg, .35)}"/><stop offset="1" stop-color="{bg}"/></linearGradient></defs>')
    b.append('<rect width="240" height="300" fill="url(#bg)"/>')
    b.append(back)
    b.append(clothing(spec["clothes"], {"cloth": spec["cloth"]}, spec.get("cx", {})))
    # neck
    b.append(f'<path d="M97 186 L97 242 C106 254 134 254 143 242 L143 186 Z" fill="{skin}"/>')
    b.append(f'<path d="M97 200 C110 216 130 216 143 200 L143 222 C130 232 110 232 97 222 Z" fill="{sk_d}" opacity=".5"/>')
    if spec.get("clothes") == "masked":
        b.append(clothing("masked", {"cloth": spec["cloth"]}, {})[len(clothing("masked", {"cloth": spec["cloth"]}, {})) - 220:] if False else "")
    b.append('<g transform="translate(0,12)">')
    # ears + head
    b.append(f'<ellipse cx="71" cy="134" rx="7" ry="12" fill="{skin}"/><ellipse cx="169" cy="134" rx="7" ry="12" fill="{skin}"/>')
    b.append(f'<path d="{FACE[jaw]}" fill="{skin}"/>')
    b.append(f'<path d="M80 150 C86 176 104 192 120 195" stroke="{sk_d}" stroke-width="3" fill="none" opacity=".25"/>')
    if spec.get("blush"):
        b.append(f'<ellipse cx="90" cy="156" rx="9" ry="5" fill="#e88a7a" opacity=".22"/><ellipse cx="150" cy="156" rx="9" ry="5" fill="#e88a7a" opacity=".22"/>')
    # beard/stubble under features
    if spec.get("beard"):
        bc = spec["beard"]
        b.append(f'<path d="M76 150 C80 184 100 198 120 200 C140 198 160 184 164 150 C156 168 142 176 120 176 C98 176 84 168 76 150 Z" fill="{bc}" opacity=".95"/>')
    if spec.get("stubble"):
        b.append(f'<path d="M80 152 C86 182 104 196 120 197 C136 196 154 182 160 152 C152 172 140 184 120 184 C100 184 88 172 80 152 Z" fill="#3a3028" opacity=".16"/>')
    # features
    b.append(brows(spec.get("brow", dark(hair_col, .3)) if not spec.get("brow_c") else spec["brow_c"], spec.get("brow_t", 3.2), spec.get("brow_a", 0), spec.get("brow_arch", 0)))
    b.append(eyes(spec.get("eyes", "normal"), spec["iris"], ink))
    b.append(f'<path d="M120 140 C117 152 114 158 121 161 C124 161.5 126 160 127 158" stroke="{sk_d}" stroke-width="2.2" fill="none" stroke-linecap="round" opacity=".7"/>')
    if spec.get("mustache"):
        mc = spec["mustache"]
        b.append(f'<path d="M104 168 C112 163 120 168 120 168 C120 168 128 163 136 168 C132 174 124 172 120 171 C116 172 108 174 104 168 Z" fill="{mc}"/>')
    b.append(mouth(spec.get("mouth", "neutral"), skin))
    if spec.get("wrinkles"):
        b.append(f'<path d="M92 150 C96 158 98 164 100 170 M148 150 C144 158 142 164 140 170 M92 108 L148 108" stroke="{sk_d}" stroke-width="1.6" fill="none" opacity=".45"/>')
        b.append(f'<path d="M86 124 C92 120 98 120 102 122 M138 122 C142 120 148 120 154 124" stroke="{sk_d}" stroke-width="1.4" fill="none" opacity=".4"/>')
    if spec.get("scarX"):
        b.append(f'<g stroke="#7a3a38" stroke-width="3.4" stroke-linecap="round" opacity=".85"><path d="M104 82 L136 116"/><path d="M136 82 L104 116"/></g>')
        b.append(f'<g stroke="#e9c9c0" stroke-width="1" stroke-linecap="round" opacity=".45"><path d="M105 83 L137 117"/><path d="M137 83 L105 117"/></g>')
    if spec.get("scar"):
        b.append(f'<path d="{spec["scar"]}" stroke="#8a4a40" stroke-width="2.6" fill="none" stroke-linecap="round" opacity=".8"/>')
    # hair/headgear front
    if spec.get("turban"):
        b.append(turban(spec["turban"]))
    elif spec.get("headwrap"):
        b.append(headwrap(spec["headwrap"]))
    else:
        b.append(front)
    if spec.get("headband"):
        b.append(f'<path d="M70 98 C96 86 144 86 170 98 L170 108 C144 96 96 96 70 108 Z" fill="{spec["headband"]}"/>')
    if spec.get("goggles"):
        b.append(f'<path d="M72 92 C100 84 140 84 168 92" stroke="#4a3a2a" stroke-width="9" fill="none"/><circle cx="102" cy="82" r="11" fill="#9ab8c0" stroke="#4a3a2a" stroke-width="4"/><circle cx="138" cy="82" r="11" fill="#9ab8c0" stroke="#4a3a2a" stroke-width="4"/>')
    if spec.get("glasses"):
        gc = spec["glasses"]
        if spec.get("gshape") == "rect":
            b.append(f'<g fill="none" stroke="{gc}" stroke-width="2.4"><rect x="82" y="118" width="32" height="24" rx="5"/><rect x="126" y="118" width="32" height="24" rx="5"/><path d="M114 126 L126 126"/><path d="M82 126 L72 122 M158 126 L168 122"/></g>')
        else:
            b.append(f'<g fill="none" stroke="{gc}" stroke-width="2.4"><circle cx="99" cy="131" r="15"/><circle cx="141" cy="131" r="15"/><path d="M114 128 Q120 124 126 128"/><path d="M84 128 L72 124 M156 128 L168 124"/></g>')
    if spec.get("earring"):
        b.append(f'<circle cx="71" cy="150" r="3.2" fill="{spec["earring"]}"/>')
    b.append('</g>')
    b.append(over)
    # photo frame polish
    b.append('<rect x="0.5" y="0.5" width="239" height="299" fill="none" stroke="#000" stroke-opacity=".08"/>')
    b.append("</svg>")
    return "".join(b)


# ---------- skin / palette ----------
SK = dict(fair="#f4d6bb", warm="#efc9a2", tan="#d8a272", brown="#b27a52", deep="#8f5d3d")
BG = dict(elric="#e6cf99", ishval="#dccaa5", amestris="#a9bbd2", xing="#a9cbb6", lansi="#e2bf84", west="#bfc99a", karsa="#d9a98e")

SPECS = [
    # name, slug, group bg, spec, appearance
    dict(name="에드워드 엘릭", slug="edward", bg=BG["elric"], skin=SK["fair"], hair="#f0c64a", style="cowlick", iris="#e0a524",
         eyes="sharp", jaw="narrow", brow_a=1.5, mouth="smirk", clothes="jacket", cloth="#1f1f26", cx=dict(scarf="#a8342b"),
         look="금빛 머리를 길게 땋아 내리고 이마에 짧은 머리카락이 솟은, 눈매가 날카로운 청년. 2년 사이 얼굴선이 조금 길어졌다."),
    dict(name="알폰스 엘릭", slug="alphonse", bg=BG["elric"], skin=SK["fair"], hair="#d9ab57", style="soft", iris="#8d7f6c",
         eyes="soft", jaw="soft", brow_t=3, mouth="soft", blush=True, clothes="sweater", cloth="#c8b08a",
         look="부드러운 갈금빛 머리와 회갈색 눈의 온화한 청년. 머리가 조금 자랐고 어깨가 넓어졌다."),
    dict(name="스카", slug="scar", bg=BG["ishval"], skin=SK["deep"], hair="#e7e4de", style="spiky", iris="#a82828",
         eyes="sharp", jaw="strong", brow_t=4, brow_a=3, brow_c="#cfcac2", mouth="frown", scarX=True, clothes="wrap", cloth="#3a3436",
         look="검게 그은 피부와 붉은 눈, 이마에 X자 흉터가 있는 흰 머리의 장신. 표정이 단단하다."),
    dict(name="스카의 형", slug="scar-brother", bg=BG["ishval"], skin=SK["brown"], hair="#44403c", style="longtied", iris="#8c2e2e",
         eyes="soft", jaw="soft", brow_t=3, mouth="soft", stubble=True, headband="#c9b48a", clothes="robe", cloth="#d6c8a6", cx=dict(trim="#8a7a52"),
         look="뒤로 묶은 긴 머리에 이마띠를 두른 학자풍의 이슈발인. 눈매가 부드럽고 말수가 적은 인상."),
    dict(name="마일즈", slug="miles", bg=BG["ishval"], skin=SK["brown"], hair="#bdb7ac", style="neat", iris="#7a3a2c",
         eyes="heavy", jaw="strong", brow_t=3.4, mouth="neutral", clothes="uniform", cloth="#2a3a5e", cx=dict(pips=3),
         look="짧게 다듬은 옅은 회색 머리와 갈색 피부, 침착한 눈의 군 장교. 군복 깃에 대령 계급장."),
    dict(name="아딘", slug="adin", bg=BG["ishval"], skin=SK["deep"], hair="#1d1a1a", style="mop", iris="#a83232",
         eyes="round", jaw="soft", mouth="smirk", blush=True, clothes="worker", cloth="#8d7c5a",
         look="헝클어진 검은 머리와 붉은 눈의 젊은 이슈발 주민. 작업복 차림에 표정이 솔직하다."),
    dict(name="자히르", slug="zahir", bg=BG["ishval"], skin=SK["deep"], hair="#e6e2da", style="elder", iris="#8e2c2c",
         eyes="heavy", jaw="strong", beard="#d9d5cc", brow_c="#cfcac2", wrinkles=True, mouth="neutral", clothes="wrap", cloth="#cdbb98",
         look="흰 수염과 주름이 깊은 이슈발의 노인. 붉은 눈이 고요하고 흰 천을 둘렀다."),
    dict(name="하심", slug="hashim", bg=BG["ishval"], skin=SK["tan"], hair="#2a221c", turban="#e8dcc0", iris="#5a3a24",
         eyes="normal", jaw="round", mustache="#2a221c", mouth="smile", clothes="vest", cloth="#d8c9a6", cx=dict(vest="#2d6a68"),
         look="흰 터번과 콧수염의 사막 상인. 웃는 얼굴이 넉살 좋고 조끼를 걸쳤다."),
    dict(name="로이 머스탱", slug="mustang", bg=BG["amestris"], skin=SK["fair"], hair="#1c1c22", style="swept", iris="#26262c",
         eyes="sharp", jaw="strong", brow_t=3.4, brow_a=1, mouth="smirk", wrinkles=False, clothes="uniform", cloth="#27385c", cx=dict(pips=0, stripe=True),
         look="비스듬히 넘긴 검은 머리와 검은 눈의 지도자. 여유 있는 미소 끝에 2년 사이 피로가 조금 내려앉았다."),
    dict(name="리자 호크아이", slug="hawkeye", bg=BG["amestris"], skin=SK["fair"], hair="#e3c176", style="updo", iris="#7b5a3a",
         eyes="sharp", jaw="narrow", brow_t=2.6, mouth="neutral", clothes="uniform", cloth="#27385c", cx=dict(pips=2),
         look="금발을 틀어 올리고 갈색 눈이 곧은 군인. 앞머리 한 가닥이 옆으로 흐르고 계급은 대위."),
    dict(name="에리히 브란트", slug="brandt", bg=BG["amestris"], skin=SK["warm"], hair="#6a6258", style="balding", iris="#6b7378",
         eyes="soft", jaw="round", glasses="#40454c", gshape="rect", brow_t=3, mouth="soft", wrinkles=True, clothes="suit", cloth="#2b2b33", cx=dict(tie="#6e2a30"),
         look="이마가 넓어진 잿빛 머리에 각진 안경을 쓴 민간 정치인. 짙은 정장에 말씨가 차분해 보인다."),
    dict(name="그라우스", slug="graus", bg=BG["amestris"], skin=SK["fair"], hair="#3a2e28", style="neat", iris="#59666f",
         eyes="sharp", jaw="strong", brow_t=3, brow_a=1.5, mouth="neutral", clothes="uniform", cloth="#27385c", cx=dict(pips=1, stripe=True),
         look="가지런히 빗은 짙은 갈색 머리와 회청색 눈의 장교. 표정이 흐트러지지 않으며 계급은 준장."),
    dict(name="바르크", slug="bark", bg=BG["amestris"], skin=SK["warm"], hair="#8b6b4a", style="neat", iris="#68786a",
         eyes="soft", jaw="narrow", brow_t=2.6, mouth="neutral", clothes="uniform", cloth="#27385c", cx=dict(pips=1),
         look="연한 갈색 머리와 회녹색 눈의 젊은 장교. 말수가 적고 시선이 곧게 앞을 향한다."),
    dict(name="린 야오", slug="lin", bg=BG["xing"], skin=SK["warm"], hair="#16161c", style="topknot", iris="#1c1a1a",
         eyes="fox", jaw="narrow", brow_t=2.6, brow_a=1, mouth="smirk", clothes="imperial", cloth="#3c2a5c",
         look="가늘게 올라간 눈과 틀어 올린 검은 머리, 금관 장식을 단 황제. 2년 사이 웃음에 무게가 붙었다."),
    dict(name="메이 창", slug="mei", bg=BG["xing"], skin=SK["warm"], hair="#16161c", style="bun", iris="#4a2f20",
         eyes="round", jaw="soft", brow_t=2.4, mouth="smile", blush=True, clothes="tunic", cloth="#2f7f78", cx=dict(trim="#e0b94a"),
         look="양쪽으로 둥글게 묶은 검은 머리와 큰 갈색 눈의 연단술사. 2년 사이 키와 표정이 한 뼘 자랐다."),
    dict(name="란팡", slug="lanfan", bg=BG["xing"], skin=SK["warm"], hair="#13151a", style="bob", iris="#16161c",
         eyes="sharp", jaw="narrow", brow_t=2.6, brow_a=2, mouth="neutral", clothes="masked", cloth="#1f2430",
         look="곧게 자른 단발의 검은 머리와 날카로운 눈. 목에 검은 복면을 내려 두른 호위무사."),
    dict(name="리엔", slug="lien", bg=BG["lansi"], skin=SK["fair"], hair="#8c8a86", style="slick", iris="#5b5148",
         eyes="soft", jaw="round", glasses="#6a5a3a", brow_t=2.6, mouth="soft", wrinkles=True, clothes="robe", cloth="#7a5a3c", cx=dict(trim="#4a3a28"),
         look="회색 머리를 뒤로 넘기고 둥근 안경을 쓴 고문서 연구자. 갈색 학자복에 먹물 냄새가 날 듯한 인상."),
    dict(name="푸룽", slug="purong", bg=BG["lansi"], skin=SK["warm"], hair="#1a1618", style="slick", iris="#2e2220",
         eyes="fox", jaw="narrow", brow_t=2.4, mouth="smirk", earring="#e0b94a", mustache="#1a1618", clothes="robe", cloth="#7a2e32", cx=dict(trim="#d6a935"),
         look="매끄럽게 넘긴 검은 머리에 금 귀걸이를 한 정보 중개인. 얇은 콧수염과 능글맞은 입꼬리가 인상적이다."),
    dict(name="샤오린", slug="xiaolin", bg=BG["west"], skin=SK["tan"], hair="#4a3426", style="swept", iris="#5a3d28",
         eyes="normal", jaw="soft", mouth="smile", blush=True, clothes="coat", cloth="#6a6b4a", cx=dict(scarf="#c8742f"),
         look="갈색 머리를 단정히 넘기고 여행용 외투를 걸친 안족 청년. 눈이 밝고 표정이 열려 있다."),
    dict(name="천루오", slug="tianluo", bg=BG["west"], skin=SK["tan"], hair="#241c18", style="buzz", iris="#3a2a1e",
         eyes="heavy", jaw="strong", brow_t=4, brow_a=2.5, mouth="frown", stubble=True, clothes="coat", cloth="#5a5238",
         look="짧게 깎은 머리에 눈썹이 짙고 턱이 단단한 안족 남자. 입을 꾹 다문 신중한 인상."),
    dict(name="루한 바이", slug="luhan", bg=BG["west"], skin=SK["fair"], hair="#15151b", style="slick", iris="#3a2a22",
         eyes="sharp", jaw="strong", brow_t=3.4, brow_a=2, mouth="neutral", clothes="robe", cloth="#e6e3da", cx=dict(trim="#3b5a8a"),
         look="뒤로 넘긴 검은 머리와 곧은 시선의 바이족 후계자. 흰 옷에 푸른 단을 둘렀고 표정이 굳었다."),
    dict(name="젠하 바이", slug="jenha", bg=BG["west"], skin=SK["warm"], hair="#76736c", style="slick", iris="#4a3a2a",
         eyes="fox", jaw="round", beard="#7b7870", mustache="#7b7870", brow_t=2.8, mouth="smirk", wrinkles=True, clothes="robe", cloth="#e2dccb", cx=dict(trim="#c9a640"),
         look="희끗한 머리와 정돈된 수염의 바이족 유력자. 부드러운 웃음 뒤에 계산이 보이고 흰 비단옷에 금단을 둘렀다."),
    dict(name="웨이 바이", slug="wei", bg=BG["west"], skin=SK["warm"], hair="#e4e1da", style="elder", iris="#5e5448",
         eyes="heavy", jaw="narrow", beard="#e4e1da", brow_c="#cfcac2", wrinkles=True, mouth="neutral", clothes="robe", cloth="#bdbab0", cx=dict(trim="#4a5f86"),
         look="흰 머리와 긴 수염이 정갈한 바이족 원로. 주름진 눈매가 엄하고 회색 예복을 입었다."),
    dict(name="카이룬", slug="kairun", bg=BG["west"], skin=SK["tan"], hair="#1a1613", style="mop", iris="#2e221a",
         eyes="sharp", jaw="narrow", brow_t=3.4, brow_a=3, stubble=True, mouth="frown", clothes="coat", cloth="#4f4636",
         look="거칠게 자란 검은 머리와 야윈 얼굴, 꺼진 눈의 안족 남자. 낡은 외투에 그늘이 짙다."),
    dict(name="나디르", slug="nadir", bg=BG["karsa"], skin=SK["tan"], hair="#6c665c", headwrap="#d7c4a0", iris="#4a3524",
         eyes="soft", jaw="strong", beard="#8a857a", brow_c="#6c665c", wrinkles=True, mouth="neutral", clothes="wrap", cloth="#b99a6e",
         look="모래빛 두건을 두르고 짧은 회색 수염을 기른 카르사의 지도자. 눈이 차분하고 신중하다."),
    dict(name="사하라", slug="sahara", bg=BG["karsa"], skin=SK["tan"], hair="#3a3028", headwrap="#e8dcc0", iris="#4a3a2a",
         eyes="soft", jaw="soft", glasses="#6a5a3a", brow_t=2.6, mouth="soft", clothes="wrap", cloth="#c8b08a",
         look="밝은 두건을 쓰고 둥근 안경을 낀 기록관리자. 조용하고 꼼꼼해 보인다."),
    dict(name="다우드", slug="daud", bg=BG["karsa"], skin=SK["brown"], hair="#1d1814", headwrap="#7a6a52", iris="#2e2218",
         eyes="heavy", jaw="strong", brow_t=4.2, brow_a=3, stubble=True, mouth="frown", clothes="wrap", cloth="#6a5a40", scar="M154 118 C158 136 158 150 154 162",
         look="어두운 두건을 두르고 눈썹이 짙은 카르사의 방어 담당. 뺨에 오래된 흉터가 있고 경계하는 표정."),
    dict(name="마지드", slug="majid", bg=BG["karsa"], skin=SK["brown"], hair="#2a221c", style="curly", iris="#3a2a1c",
         eyes="round", jaw="soft", goggles=True, brow_t=3, mouth="smile", stubble=True, clothes="worker", cloth="#8a6f4a",
         look="곱슬머리 위에 보안경을 얹은 카르사의 기술자. 손재주 좋은 사람다운 느긋한 웃음."),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in SPECS:
        (OUT / f"{spec['slug']}.svg").write_text(make(spec), encoding="utf-8", newline="\n")
    cfg_raw = CONFIG.read_bytes().decode("utf-8")
    crlf = "\r\n" in cfg_raw
    cfg = json.loads(cfg_raw.replace("\r\n", "\n"))
    table = {s["name"]: s for s in SPECS}
    missing = [p["name"] for p in cfg["publicCharacters"] if p["name"] not in table]
    assert not missing, missing
    for person in cfg["publicCharacters"]:
        spec = table[person["name"]]
        person["portrait"] = f"portraits/{spec['slug']}.svg"
        person["appearance"] = spec["look"]
    text = json.dumps(cfg, ensure_ascii=False, indent=2) + "\n"
    CONFIG.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))
    print(f"portraits={len(SPECS)} -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
