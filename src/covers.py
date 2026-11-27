"""Draws the note covers as two-ink Riso line art (1200x630, the Open Graph ratio).

Every drawing is printed twice: a pink plate (multiplied, a few pixels off register) under deep-ink line work,
with Riso green as the flood ink. Generic, self-drawn shapes only: no third-party marks.
Run: python3 src/covers.py  (writes docs/notes/<slug>/<cover>.svg)
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INK, GREEN, PINK, PAPER, PAPER2, OVER = '#0e2a1f', '#00a95c', '#ff48b0', '#fbfbf8', '#f2f3ec', '#5b2e4a'
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"
SANS = "'Arial', 'Helvetica', sans-serif"


def svg(body: str, title: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630" role="img">
<title>{title}</title>
<defs>
  <pattern id="dots" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="7" cy="7" r="2.6" fill="{PINK}"/></pattern>
  <pattern id="dotsG" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="6" cy="6" r="2.2" fill="{GREEN}"/></pattern>
  <pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="10" stroke="{INK}" stroke-width="2"/></pattern>
</defs>
<rect width="1200" height="630" fill="{PAPER}"/>
{reg_marks()}
{body}
</svg>
'''


def reg_marks() -> str:
    out = []
    for x, y in ((46, 46), (1154, 46), (46, 584), (1154, 584)):
        out.append(f'<g stroke="{INK}" stroke-width="2" fill="none"><circle cx="{x}" cy="{y}" r="11"/>'
                   f'<line x1="{x-19}" y1="{y}" x2="{x+19}" y2="{y}"/><line x1="{x}" y1="{y-19}" x2="{x}" y2="{y+19}"/></g>')
    return '\n'.join(out)


def plate(shape: str, dx=12, dy=9) -> str:
    """Pink second pass under a shape, multiplied and off register."""
    return f'<g transform="translate({dx} {dy})" style="mix-blend-mode:multiply" opacity="0.9">{shape}</g>'


def app_card(x, y, s=1.0, fill=GREEN, glyph='chat', dashed=False) -> str:
    """A generic rounded app card (120 units square) with a self-drawn glyph, scaled as one group."""
    dash = ' stroke-dasharray="10 8"' if dashed else ''
    g = {
        'chat': f'<path d="M32 38 h56 a10 10 0 0 1 10 10 v24 a10 10 0 0 1 -10 10 h-30 l-16 14 v-14 h-10 a10 10 0 0 1 -10 -10 v-24 a10 10 0 0 1 10 -10z" fill="{PAPER}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>',
        'note': f'<rect x="34" y="28" width="52" height="64" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="4"/><path d="M44 48 h32 M44 62 h32 M44 76 h20" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>',
        'shield': f'<path d="M60 26 l30 12 v22 c0 22 -14 34 -30 40 c-16 -6 -30 -18 -30 -40 v-22z" fill="{PAPER}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/><path d="M48 62 l9 9 l17 -18" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
        'camera': f'<rect x="26" y="40" width="68" height="48" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="4"/><circle cx="60" cy="64" r="13" fill="none" stroke="{INK}" stroke-width="4"/><path d="M46 40 l6 -9 h16 l6 9" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>',
        'key': f'<circle cx="44" cy="60" r="15" fill="{PAPER}" stroke="{INK}" stroke-width="4"/><path d="M59 60 h34 M84 60 v13 M75 60 v9" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>',
    }[glyph]
    return (f'<g transform="translate({x} {y}) scale({s})"><rect width="120" height="120" rx="28" fill="{fill}" stroke="{INK}" stroke-width="4.5"{dash}/>'
            + g + '</g>')


def secure_env() -> str:
    lines = []
    y0 = 172
    widths = [300, 250, 340, 200, 380, 260, 310, 220]
    for i, w in enumerate(widths):
        y = y0 + i * 40
        if i == 3:
            continue
        indent = 40 if 0 < i < 7 else 0
        lines.append(f'<rect x="{170+indent}" y="{y}" width="{w-indent}" height="12" rx="6" fill="{INK}" opacity="0.22"/>')
    marked = (f'<rect x="196" y="{y0+3*40-20}" width="396" height="52" rx="10" fill="{PINK}" opacity="0.85" style="mix-blend-mode:multiply"/>'
              f'<text x="214" y="{y0+3*40+14}" font-family="{MONO}" font-size="27" font-weight="700" fill="{INK}">REQUIRE_SECURE_ENV = 1</text>')
    sheet = (f'<path d="M130 100 h420 l60 60 v380 a18 18 0 0 1 -18 18 h-462 a18 18 0 0 1 -18 -18 v-422 a18 18 0 0 1 18 -18z" fill="{PAPER}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<path d="M550 100 v60 h60" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<text x="160" y="146" font-family="{MONO}" font-size="22" fill="{INK}" opacity="0.75">AndroidManifest.xml</text>')
    sheet_plate = plate(f'<path d="M130 100 h420 l60 60 v380 a18 18 0 0 1 -18 18 h-462 a18 18 0 0 1 -18 -18 v-422 a18 18 0 0 1 18 -18z" fill="{PINK}"/>', 14, 11)
    container = (f'<rect x="812" y="120" width="300" height="400" rx="46" fill="url(#dotsG)" opacity="0.35"/>'
                 f'<rect x="812" y="120" width="300" height="400" rx="46" fill="none" stroke="{INK}" stroke-width="5" stroke-dasharray="18 14"/>'
                 + app_card(842, 170, 0.95, GREEN, 'chat') + app_card(972, 170, 0.95, GREEN, 'note')
                 + app_card(842, 320, 0.95, PAPER2, 'camera', dashed=True))
    blocked = (plate(f'<rect x="660" y="300" width="125" height="125" rx="30" fill="{PINK}"/>', 10, 8)
               + app_card(656, 296, 1.04, GREEN, 'shield')
               + f'<path d="M800 280 v170" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
               + f'<path d="M780 458 c-30 28 -90 30 -120 4" fill="none" stroke="{INK}" stroke-width="4" stroke-dasharray="8 8"/>'
               + f'<path d="M668 452 l-9 12 l14 4" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    sun = f'<circle cx="1040" cy="560" r="70" fill="url(#dots)" opacity="0.85"/>'
    return svg(sun + sheet_plate + sheet + ''.join(lines) + marked + container + blocked,
               'Manifest with REQUIRE_SECURE_ENV and an app kept outside a container')


def insets() -> str:
    phone = lambda x, label, ok: (
        plate(f'<rect x="{x}" y="70" width="300" height="500" rx="46" fill="{PINK}"/>', 12, 10)
        + f'<rect x="{x}" y="70" width="300" height="500" rx="46" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
        + f'<rect x="{x+18}" y="92" width="264" height="36" rx="10" fill="url(#hatch)" opacity="0.55"/>'
        + f'<rect x="{x+18}" y="512" width="264" height="36" rx="10" fill="url(#hatch)" opacity="0.55"/>'
        + f'<rect x="{x+130}" y="527" width="40" height="6" rx="3" fill="{INK}"/>'
        + (
            # content sits inside the safe area
            f'<rect x="{x+28}" y="142" width="244" height="356" rx="20" fill="{GREEN}" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="{x+50}" y="166" width="150" height="14" rx="7" fill="{INK}"/>'
            f'<rect x="{x+50}" y="196" width="200" height="10" rx="5" fill="{PAPER}"/><rect x="{x+50}" y="216" width="170" height="10" rx="5" fill="{PAPER}"/>'
            f'<rect x="{x+50}" y="440" width="200" height="38" rx="12" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>'
            if ok else
            # content slides under both bars
            f'<rect x="{x+28}" y="96" width="244" height="448" rx="20" fill="{PINK}" opacity="0.7" stroke="{INK}" stroke-width="4" stroke-dasharray="12 9" style="mix-blend-mode:multiply"/>'
            f'<rect x="{x+50}" y="104" width="150" height="14" rx="7" fill="{INK}"/>'
            f'<rect x="{x+50}" y="500" width="200" height="38" rx="12" fill="{PAPER}" stroke="{INK}" stroke-width="4" stroke-dasharray="8 6"/>'
        )
        + f'<rect x="{x+60}" y="586" width="180" height="0.1"/>'
        + f'<text x="{x+150}" y="612" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="700" fill="{INK}">{label}</text>'
    )
    arrow = (f'<path d="M560 320 h70" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
             f'<path d="M612 300 l22 20 l-22 20" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    ruler = ''.join(f'<line x1="1060" y1="{y}" x2="{1060 + (22 if i % 4 == 0 else 12)}" y2="{y}" stroke="{INK}" stroke-width="3"/>' for i, y in enumerate(range(90, 560, 16)))
    ruler += f'<line x1="1060" y1="88" x2="1060" y2="556" stroke="{INK}" stroke-width="3"/>'
    sun = f'<circle cx="150" cy="120" r="80" fill="url(#dots)" opacity="0.8"/>'
    return svg(sun + phone(220, 'Before: under the bars', False) + arrow + phone(700, 'After: inside the insets', True) + ruler,
               'An older app drawn under the system bars, then inside the insets')


def one_uid() -> str:
    big = (plate('<rect x="110" y="110" width="560" height="400" rx="44" fill="#ff48b0"/>', 14, 11)
           + f'<rect x="110" y="110" width="560" height="400" rx="44" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
           + f'<rect x="138" y="138" width="504" height="344" rx="30" fill="url(#dotsG)" opacity="0.3"/>'
           + f'<line x1="390" y1="150" x2="390" y2="470" stroke="{INK}" stroke-width="4" stroke-dasharray="14 12"/>'
           + app_card(185, 200, 1.25, GREEN, 'chat') + app_card(450, 200, 1.25, GREEN, 'chat')
           + f'<rect x="200" y="380" width="120" height="16" rx="8" fill="{INK}" opacity="0.25"/><rect x="465" y="380" width="120" height="16" rx="8" fill="{INK}" opacity="0.25"/>'
           + f'<rect x="270" y="532" width="240" height="50" rx="25" fill="{INK}"/>'
           + f'<text x="390" y="565" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="700" fill="{PAPER}">one UID</text>')
    small = lambda y, label: (
        f'<rect x="760" y="{y}" width="340" height="190" rx="34" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
        + app_card(790, y + 38, 0.95, GREEN, 'chat')
        + f'<text x="928" y="{y+86}" font-family="{SANS}" font-size="25" font-weight="700" fill="{INK}">{label}</text>'
        + f'<text x="928" y="{y+120}" font-family="{SANS}" font-size="21" fill="{INK}" opacity="0.75">own UID</text>')
    sun = f'<circle cx="1110" cy="560" r="64" fill="url(#dots)" opacity="0.85"/>'
    return svg(sun + big + small(100, 'Main user') + small(340, 'Profile'),
               'Two copies sharing one UID beside a main user and a profile with their own')


def accounts() -> str:
    def space(x, n):
        return (plate(f'<rect x="{x}" y="150" width="230" height="330" rx="38" fill="{PINK}"/>', 11, 9)
                + f'<rect x="{x}" y="150" width="230" height="330" rx="38" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
                + f'<text x="{x+115}" y="200" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="700" fill="{INK}">Account {n}</text>'
                + app_card(x + 20, 228, 0.74, GREEN, 'chat') + app_card(x + 121, 228, 0.74, GREEN if n != 3 else PAPER2, 'note', dashed=(n == 3))
                + f'<line x1="{x+24}" y1="352" x2="{x+206}" y2="352" stroke="{INK}" stroke-width="3" stroke-dasharray="10 8"/>'
                + app_card(x + 55, 368, 0.98, PAPER, 'key'))
    licence = (f'<rect x="900" y="120" width="210" height="300" rx="16" fill="{PAPER2}" stroke="{INK}" stroke-width="5" transform="rotate(4 1005 270)"/>'
               f'<g transform="rotate(4 1005 270)"><text x="926" y="176" font-family="{SANS}" font-size="27" font-weight="700" fill="{INK}">Apache</text>'
               f'<text x="926" y="208" font-family="{SANS}" font-size="27" font-weight="700" fill="{INK}">License 2.0</text>'
               + ''.join(f'<rect x="926" y="{236 + i*26}" width="{150 - (i % 3)*30}" height="10" rx="5" fill="{INK}" opacity="0.25"/>' for i in range(6))
               + f'<circle cx="1060" cy="392" r="24" fill="{GREEN}" stroke="{INK}" stroke-width="4"/><path d="M1049 392 l8 8 l14 -15" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g>')
    sun = f'<circle cx="140" cy="540" r="70" fill="url(#dots)" opacity="0.85"/>'
    return svg(sun + space(110, 1) + space(370, 2) + space(630, 3) + licence,
               'Three Account spaces, each with its own sign-in key, beside a licence sheet')


def lock(x, y, s=1.0, fill=GREEN) -> str:
    """Small padlock, 40 units wide, top-left at x,y."""
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M10 18 v-6 a10 10 0 0 1 20 0 v6" fill="none" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="4" y="18" width="32" height="24" rx="6" fill="{fill}" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="20" cy="30" r="3.5" fill="{INK}"/></g>')


def chunked_backup() -> str:
    cells = []
    x0, w, gap = 90, 150, 16
    for i in range(6):
        x = x0 + i * (w + gap)
        y = 250
        cells.append(plate(f'<rect x="{x}" y="{y}" width="{w}" height="150" rx="22" fill="{PINK}"/>', 8, 7))
        last = i == 5
        cells.append(f'<rect x="{x}" y="{y}" width="{w}" height="150" rx="22" fill="{PAPER}" stroke="{INK}" stroke-width="4.5"/>')
        cells.append(f'<rect x="{x+16}" y="{y+22}" width="{w-32}" height="12" rx="6" fill="{INK}" opacity="0.22"/>'
                     f'<rect x="{x+16}" y="{y+44}" width="{w-60}" height="12" rx="6" fill="{INK}" opacity="0.22"/>')
        cells.append(lock(x + w / 2 - 20, y + 74, 1.0, GREEN if not last else PINK))
        cells.append(f'<circle cx="{x+30}" cy="{y-26}" r="22" fill="{INK}"/>'
                     f'<text x="{x+30}" y="{y-17}" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="700" fill="{PAPER}">{i+1}</text>')
    fx = x0 + 5 * (w + gap)
    flag = (f'<path d="M{fx+w-30} 250 v-90" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M{fx+w-30} 160 h58 l-14 20 l14 20 h-58z" fill="{GREEN}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>')
    stray = (f'<g transform="translate(560 470) rotate(-8)"><rect width="150" height="100" rx="18" fill="{PAPER2}" stroke="{INK}" stroke-width="4.5" stroke-dasharray="12 9"/>'
             f'<text x="75" y="62" text-anchor="middle" font-family="{SANS}" font-size="30" font-weight="700" fill="{INK}">9</text>'
             f'<path d="M-8 -8 L158 108 M158 -8 L-8 108" stroke="{PINK}" stroke-width="8" stroke-linecap="round" opacity="0.9"/></g>')
    bar = f'<rect x="{x0}" y="452" width="{6*w+5*gap}" height="12" rx="6" fill="url(#dotsG)"/>'
    sun = f'<circle cx="1110" cy="100" r="70" fill="url(#dots)" opacity="0.85"/>'
    return svg(sun + ''.join(cells) + flag + bar + stray,
               'A backup cut into numbered chunks, each sealed, the last one flagged and a stray chunk crossed out')


def push_closed() -> str:
    cloud = (f'<path d="M150 190 a52 52 0 0 1 98 -22 a42 42 0 0 1 70 30 a34 34 0 0 1 -6 66 h-148 a46 46 0 0 1 -14 -74z" fill="{PAPER2}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    env = (f'<g transform="translate(430 150)">' + plate(f'<rect width="170" height="116" rx="16" fill="{PINK}"/>', 10, 8)
           + f'<rect width="170" height="116" rx="16" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
           + f'<path d="M6 10 L85 70 L164 10" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></g>')
    arrow1 = (f'<path d="M330 215 h86" stroke="{INK}" stroke-width="6" stroke-linecap="round" stroke-dasharray="4 14"/>'
              f'<path d="M404 195 l22 20 l-22 20" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    run = (f'<g transform="translate(120 340)">' + app_card(0, 0, 1.25, GREEN, 'chat')
           + f'<text x="75" y="190" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="700" fill="{INK}">running</text></g>')
    closed = (f'<g transform="translate(470 340)"><g opacity="0.55">' + app_card(0, 0, 1.25, PAPER2, 'chat', dashed=True) + '</g>'
              + f'<text x="75" y="190" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="700" fill="{INK}">closed</text></g>')
    down1 = (f'<path d="M500 280 C 500 310 300 300 200 336" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
             f'<path d="M520 280 C 540 310 540 320 545 336" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-dasharray="3 12"/>')
    notif = (f'<g transform="translate(800 330)">' + plate(f'<rect width="300" height="130" rx="24" fill="{PINK}"/>', 10, 8)
             + f'<rect width="300" height="130" rx="24" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
             + f'<circle cx="46" cy="50" r="22" fill="{GREEN}" stroke="{INK}" stroke-width="4"/>'
             + f'<text x="84" y="48" font-family="{MONO}" font-size="22" font-weight="700" fill="{INK}">Chat #1</text>'
             + f'<rect x="84" y="64" width="190" height="12" rx="6" fill="{INK}" opacity="0.28"/><rect x="84" y="88" width="130" height="12" rx="6" fill="{INK}" opacity="0.28"/></g>')
    link = f'<path d="M640 410 h140" stroke="{INK}" stroke-width="5" stroke-dasharray="10 9" stroke-linecap="round"/>'
    sun = f'<circle cx="1080" cy="130" r="72" fill="url(#dots)" opacity="0.85"/>'
    return svg(sun + cloud + arrow1 + env + down1 + run + closed + link + notif,
               'A message from the cloud to a running copy and a closed copy, ending in a notification that names the copy')


def fgs_types() -> str:
    def tile(x, label, sub, fill, passthrough=False):
        dash = ' stroke-dasharray="14 10"' if passthrough else ''
        return (plate(f'<rect x="{x}" y="150" width="230" height="330" rx="34" fill="{PINK}"/>', 10, 8)
                + f'<rect x="{x}" y="150" width="230" height="330" rx="34" fill="{PAPER}" stroke="{INK}" stroke-width="5"{dash}/>'
                + f'<rect x="{x+18}" y="170" width="194" height="46" rx="14" fill="{fill}" stroke="{INK}" stroke-width="4"/>'
                + f'<circle cx="{x+40}" cy="193" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
                + f'<rect x="{x+60}" y="187" width="130" height="11" rx="5" fill="{INK}" opacity="0.5"/>'
                + app_card(x + 55, 250, 0.98, GREEN if not passthrough else PAPER2, 'shield' if label == 'specialUse' else ('note' if label == 'dataSync' else 'camera'), dashed=passthrough)
                + f'<text x="{x+115}" y="420" text-anchor="middle" font-family="{MONO}" font-size="24" font-weight="700" fill="{INK}">{label}</text>'
                + f'<text x="{x+115}" y="452" text-anchor="middle" font-family="{SANS}" font-size="21" fill="{INK}" opacity="0.75">{sub}</text>')
    sun = f'<circle cx="1110" cy="90" r="64" fill="url(#dots)" opacity="0.85"/>'
    return (svg(sun + tile(70, 'specialUse', 'keep copies', GREEN) + tile(330, 'specialUse', 'push', GREEN)
                + tile(590, 'dataSync', 'backup', PAPER2) + tile(850, 'asked by app', 'passed on', PAPER2, True),
                'Four foreground services, each with one type: special use twice, data sync, and the type a copied app asks for'))


def biometric() -> str:
    phone = (plate(f'<rect x="150" y="60" width="320" height="520" rx="48" fill="{PINK}"/>', 12, 10)
             + f'<rect x="150" y="60" width="320" height="520" rx="48" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
             + app_card(170, 96, 0.9, GREEN, 'chat', dashed=True)
             + f'<rect x="190" y="270" width="240" height="250" rx="30" fill="{PAPER2}" stroke="{INK}" stroke-width="5"/>'
             + ''.join(f'<circle cx="310" cy="410" r="{r}" fill="none" stroke="{INK}" stroke-width="4" stroke-dasharray="{d}"/>' for r, d in ((24, '9 6'), (42, '14 8'), (60, '20 10')))
             + f'<rect x="230" y="296" width="160" height="14" rx="7" fill="{INK}"/>')
    box = (plate(f'<rect x="640" y="190" width="300" height="250" rx="34" fill="{PINK}"/>', 12, 9)
           + f'<rect x="640" y="190" width="300" height="250" rx="34" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
           + ''.join(f'<circle cx="790" cy="320" r="{r}" fill="none" stroke="{INK}" stroke-width="4" stroke-dasharray="{d}"/>' for r, d in ((20, '8 6'), (36, '12 8'), (52, '18 9')))
           + f'<text x="790" y="236" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="700" fill="{INK}">system</text>')
    out = (f'<path d="M470 330 h150" stroke="{INK}" stroke-width="5" stroke-dasharray="3 12" stroke-linecap="round"/>'
           f'<path d="M940 320 h130" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
           f'<path d="M1048 300 l24 20 l-24 20" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
           f'<circle cx="1124" cy="320" r="34" fill="{GREEN}" stroke="{INK}" stroke-width="4.5"/>'
           f'<path d="M1108 320 l12 12 l20 -24" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    sun = f'<circle cx="980" cy="540" r="66" fill="url(#dots)" opacity="0.85"/>'
    return svg(sun + phone + box + out, 'A system fingerprint prompt over an app copy, the biometric data kept in a sealed system box, and only a yes passing out')


def bidi() -> str:
    word = '\u0627\u0644\u0646\u0633\u062e\u0629'
    def row(y, num, ok, tag):
        box = (plate(f'<rect x="150" y="{y}" width="640" height="150" rx="30" fill="{PINK}"/>', 10, 8)
               + f'<rect x="150" y="{y}" width="640" height="150" rx="30" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
               + f'<text x="750" y="{y+96}" text-anchor="end" font-family="{SANS}" font-size="70" font-weight="700" fill="{INK}">{word}</text>')
        if ok:
            box += (f'<rect x="318" y="{y+36}" width="140" height="80" rx="16" fill="none" stroke="{GREEN}" stroke-width="5" stroke-dasharray="10 8"/>'
                    f'<text x="388" y="{y+96}" text-anchor="middle" font-family="{MONO}" font-size="60" font-weight="700" fill="{INK}">{num}</text>'
                    f'<circle cx="640" cy="{y+75}" r="0" fill="none"/>')
        else:
            box += (f'<text x="388" y="{y+96}" text-anchor="middle" font-family="{MONO}" font-size="60" font-weight="700" fill="{INK}">{num}</text>'
                    f'<path d="M328 {y+112} L448 {y+38}" stroke="{PINK}" stroke-width="9" stroke-linecap="round" opacity="0.9"/>')
        box += f'<text x="170" y="{y+44}" font-family="{SANS}" font-size="28" font-weight="700" fill="{INK}" opacity="0.75">{tag}</text>'
        return box
    first = row(100, '3#', False, 'before')
    second = row(330, '#3', True, 'after')
    code = (f'<g transform="translate(520 500)"><rect width="270" height="64" rx="16" fill="{INK}"/>'
            f'<text x="135" y="42" text-anchor="middle" font-family="{MONO}" font-size="25" font-weight="700" fill="{PAPER}">U+2066 #3 U+2069</text></g>')
    arrow = (f'<path d="M470 262 v50" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
             f'<path d="M452 296 l18 20 l18 -20" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    sun = f'<circle cx="1030" cy="150" r="72" fill="url(#dots)" opacity="0.85"/>'
    return svg(sun + first + second + arrow + code,
               'A copy name in Arabic script with the number sign on the wrong side, and the same name fixed by an isolate')


COVERS = {
    'notes/require-secure-env/secure-env-opt-out.svg': secure_env,
    'notes/android-15-16-app-cloners/android-15-16-insets.svg': insets,
    'notes/how-app-copies-stay-separate/copies-one-uid.svg': one_uid,
    'notes/microg-in-an-app-cloner/microg-account-spaces.svg': accounts,
    'notes/chunked-backup-encryption/chunked-backup-chunks.svg': chunked_backup,
    'notes/push-notifications-in-app-clones/push-closed-clone.svg': push_closed,
    'notes/foreground-service-types-app-cloner/foreground-service-types.svg': fgs_types,
    'notes/biometric-prompts-in-app-clones/biometric-prompt-copy.svg': biometric,
    'notes/copy-number-right-to-left-text/copy-number-bidi.svg': bidi,
}

if __name__ == '__main__':
    for rel, fn in COVERS.items():
        out = ROOT / 'docs' / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(fn())
        print('wrote', out.relative_to(ROOT))
