"""Renders the Open Graph images (1200x630 PNG) into docs/og/ with headless Chrome via Playwright.

Run after build.py: python3 src/og.py
Needs: pip install playwright, and Google Chrome installed (uses channel='chrome').
"""
import html
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
FONTS = (DOCS / 'assets/fonts').as_uri()

TEMPLATE = '''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: B; font-weight: 200 800; src: url('{fonts}/bricolage-wght.woff2'); }}
@font-face {{ font-family: V; font-weight: 500; src: url('{fonts}/be-vietnam-500.woff2'); }}
* {{ margin: 0; box-sizing: border-box; }}
body {{ width: 1200px; height: 630px; background: #fbfbf8; color: #0e2a1f; font-family: V, sans-serif; position: relative; overflow: hidden; }}
.grain {{ position: absolute; inset: 0; opacity: .18; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .1 0 0 0 0 .14 0 0 0 0 .12 0 0 0 .5 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }}
.bar {{ position: absolute; left: 0; right: 0; bottom: 0; height: 22px; background: #00a95c; border-top: 4px solid #0e2a1f; }}
.bar::after {{ content: ''; position: absolute; left: 0; right: 0; top: -12px; height: 4px; background: #ff48b0; transform: translate(6px, 0); }}
.brand {{ position: absolute; left: 64px; top: 56px; display: flex; align-items: center; gap: 18px; font: 800 34px/1 B; letter-spacing: -.03em; }}
.brand img {{ width: 64px; height: 64px; border-radius: 16px; box-shadow: 5px 4px 0 rgba(255,72,176,.9); }}
.brand small {{ display: block; font: 500 20px/1.2 V; letter-spacing: 0; color: #2c4a40; margin-top: 6px; }}
h1 {{ position: absolute; left: 64px; top: 190px; width: {tw}px; font: 800 {fs}px/1.02 B; letter-spacing: -.035em; }}
.art {{ position: absolute; right: 36px; top: 150px; width: {aw}px; }}
.art img {{ width: 100%; }}
.kick {{ position: absolute; left: 64px; bottom: 64px; font: 500 22px/1.3 V; color: #2c4a40; }}
</style></head><body><div class="grain"></div>
<div class="brand"><img src="{icon}"><span>Duo Clone<small>{sub}</small></span></div>
<h1>{title}</h1>
<div class="art">{art}</div>
<p class="kick">{kick}</p>
<div class="bar"></div>
</body></html>'''


def render(pg, out: str, title: str, sub: str, art: str, kick: str, fs=58, tw=600, aw=560):
    doc = TEMPLATE.format(fonts=FONTS, icon=(DOCS / 'assets/icon-192.png').as_uri(), title=html.escape(title),
                          sub=html.escape(sub), art=art, kick=html.escape(kick), fs=fs, tw=tw, aw=aw)
    tmp = ROOT / 'src/.og.html'
    tmp.write_text(doc)
    pg.goto(tmp.as_uri())
    pg.wait_for_timeout(250)
    pg.screenshot(path=str(DOCS / 'og' / out))
    tmp.unlink()
    print('og/' + out)


def main():
    (DOCS / 'og').mkdir(exist_ok=True)
    notes = []
    for p in sorted((ROOT / 'src/pages').glob('notes-*.html')):
        meta = json.loads(p.read_text().split('\n---\n', 1)[0])
        notes.append(meta)
    with sync_playwright() as p:
        b = p.chromium.launch(channel='chrome')
        pg = b.new_page(viewport={'width': 1200, 'height': 630})
        for n in notes:
            slug = n['path'].strip('/').split('/')[-1]
            cover = (DOCS / n['path'] / n['cover']).as_uri()
            render(pg, slug + '.png', n['h1'], 'Developer notes by XLAB', f'<img src="{cover}">',
                   'xlabcompany.github.io/duoclone', fs=48 if len(n['h1']) < 56 else 42, tw=500, aw=560)
        icon = (DOCS / 'assets/icon-512.png').as_uri()
        press = (f'<div style="position:relative;width:300px;height:300px;margin:40px 0 0 160px">'
                 f'<div style="position:absolute;inset:0;border-radius:70px;background:#ff48b0;transform:translate(16px,13px);mix-blend-mode:multiply"></div>'
                 f'<img src="{icon}" style="position:relative;width:300px;height:300px;border-radius:70px;border:4px solid #0e2a1f"></div>')
        render(pg, 'home.png', 'The developer page for the Android app cloner', 'Developer page by XLAB', press,
               'Release notes · Developer notes · Official channel', fs=62, tw=620, aw=520)
        render(pg, 'notes.png', 'Developer notes: how an Android app cloner works', 'Developer notes by XLAB', press,
               'Platform rules, limits and what each Android release changed', fs=60, tw=620, aw=520)
        render(pg, 'changelog.png', 'Duo Clone changelog: what changed in each version', 'Release notes', press,
               'Newest first · Dates in GMT+7', fs=60, tw=620, aw=520)
        b.close()


if __name__ == '__main__':
    main()
