"""Builds the static GitHub Pages site in docs/ from src/pages/*.html and src/releases.json.

Each page file starts with a JSON header, then a line with ---, then the page body.
Run: python3 src/build.py        (then python3 src/og.py to redraw the Open Graph images)
No dependencies beyond the Python standard library.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
SITE = 'https://xlabcompany.github.io/duoclone/'
REPO = 'https://github.com/XLABCOMPANY/duoclone'
APP_SITE = 'https://duoclone.com/'
# Entity homes: XLAB lives at xlabcompany.com, the app at duoclone.com. This site references their @id nodes
# (the same ids those sites publish) instead of minting duplicates.
ORG_ID = 'https://xlabcompany.com/#organization'
WEBSITE_ID = SITE + '#website'
APP_ID = 'https://duoclone.com/#app'

ICONS = {
    'ARROW': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'GITHUB': '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.9 1.52 2.34 1.08 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.02A9.6 9.6 0 0 1 12 6.84c.85 0 1.71.11 2.51.34 1.91-1.29 2.75-1.02 2.75-1.02.55 1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.85v2.74c0 .27.18.58.69.48A10 10 0 0 0 12 2z"/></svg>',
    'PLAY': '<svg viewBox="0 0 26 26" aria-hidden="true"><path d="M7 4.5v17l14-8.5z" fill="#00a95c" stroke="#0e2a1f" stroke-width="2" stroke-linejoin="round" stroke-dasharray="3.2 2.4"/></svg>',
}


def feature_icon(paths: str, plate: str) -> str:
    """32px line glyph in deep ink over an off-register pink plate."""
    return (f'<svg viewBox="0 0 36 36" aria-hidden="true"><g transform="translate(3 3)" fill="#ff48b0" opacity=".9" style="mix-blend-mode:multiply">{plate}</g>'
            f'<g fill="none" stroke="#0e2a1f" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">{paths}</g></svg>')


FEATURES = {
    'F_COPY': feature_icon('<rect x="9" y="4" width="18" height="18" rx="5" stroke-dasharray="3.5 3"/><rect x="4" y="10" width="18" height="18" rx="5" fill="#00a95c"/>', '<rect x="4" y="10" width="18" height="18" rx="5"/>'),
    'F_ACCOUNT': feature_icon('<circle cx="12" cy="11" r="4.5"/><path d="M4 26c1-5 4.5-7.5 8-7.5s7 2.5 8 7.5"/><circle cx="23.5" cy="10" r="3.5"/><path d="M22 17c3.5 0 6.5 2 7.5 6.5"/>', '<circle cx="12" cy="11" r="4.5"/>'),
    'F_LOCK': feature_icon('<rect x="6" y="14" width="20" height="15" rx="4" fill="#00a95c"/><path d="M10.5 14v-4a5.5 5.5 0 0 1 11 0v4"/><path d="M16 20v3.5"/>', '<rect x="6" y="14" width="20" height="15" rx="4"/>'),
    'F_BACKUP': feature_icon('<path d="M5 12h22v14a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3z"/><path d="M3.5 7h25v5h-25z" fill="#00a95c"/><path d="M16 16v9M12 21l4 4 4-4"/>', '<path d="M5 12h22v14a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3z"/>'),
    'F_METER': feature_icon('<path d="M4 22a12 12 0 0 1 24 0"/><path d="M16 22l6-7"/><circle cx="16" cy="22" r="2.5" fill="#00a95c"/><path d="M4 27h24"/>', '<path d="M4 22a12 12 0 0 1 24 0z"/>'),
    'F_BUBBLE': feature_icon('<circle cx="20" cy="12" r="7" fill="#00a95c"/><rect x="4" y="16" width="14" height="13" rx="4" stroke-dasharray="3 2.6"/>', '<circle cx="20" cy="12" r="7"/>'),
    'F_EDIT': feature_icon('<rect x="4" y="8" width="18" height="18" rx="5" fill="#00a95c"/><path d="M19 22l1.2-5 8-8a2.3 2.3 0 0 1 3.3 3.3l-8 8z" fill="#fbfbf8"/>', '<rect x="4" y="8" width="18" height="18" rx="5"/>'),
    'F_GLOBE': feature_icon('<circle cx="16" cy="16" r="12"/><path d="M4 16h24M16 4c4 3.5 5.5 8 5.5 12s-1.5 8.5-5.5 12c-4-3.5-5.5-8-5.5-12S12 7.5 16 4z"/>', '<circle cx="16" cy="16" r="12"/>'),
}


def load_page(path: Path) -> dict:
    head, body = path.read_text().split('\n---\n', 1)
    meta = json.loads(head)
    meta['body'] = body
    meta['source'] = path.name
    return meta


def fmt_date(iso: str) -> str:
    d = date.fromisoformat(iso)
    return f'{d.day} {d.strftime("%B")} {d.year}'


def word_count(body: str) -> int:
    text = re.sub(r'<pre>.*?</pre>', ' ', body, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    return len(re.findall(r"[A-Za-z0-9][\w'’.-]*", html.unescape(text)))


def rel(depth: int) -> str:
    return '../' * depth


def fill_tokens(text: str, extra: dict) -> str:
    tokens = {**{f'ICON_{k}': v for k, v in ICONS.items()}, **FEATURES, **extra}
    for k, v in tokens.items():
        text = text.replace('{{' + k + '}}', v)
    left = re.findall(r'\{\{[A-Z_]+\}\}', text)
    assert not left, f'unfilled tokens: {left}'
    return text


# ---------------------------------------------------------------- JSON-LD

def org() -> dict:
    return {'@type': 'Organization', '@id': ORG_ID, 'name': 'XLAB', 'url': 'https://xlabcompany.com/'}


def website() -> dict:
    return {'@type': 'WebSite', '@id': WEBSITE_ID, 'url': SITE, 'name': 'Duo Clone developer page',
            'inLanguage': 'en', 'publisher': {'@id': ORG_ID}}


def app() -> dict:
    # No offers, prices or ratings: the app is not on sale here and nothing is invented.
    return {'@type': 'MobileApplication', '@id': APP_ID, 'name': 'Duo Clone', 'operatingSystem': 'Android',
            'applicationCategory': 'UtilitiesApplication', 'url': APP_SITE,
            'description': 'An Android app cloner for running multiple accounts of the same app on one phone.',
            'image': SITE + 'assets/icon-512.png', 'author': {'@id': ORG_ID}, 'publisher': {'@id': ORG_ID},
            'sameAs': [REPO]}


def crumbs(items: list) -> dict:
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + p} for i, (n, p) in enumerate(items)]}


def jsonld(graph: list) -> str:
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)
    return f'<script type="application/ld+json">\n{data}\n</script>'


# ---------------------------------------------------------------- layout

NAV = [('Home', ''), ('Notes', 'notes/'), ('Changelog', 'changelog/')]


def header(depth: int, current: str) -> str:
    r = rel(depth)
    links = ''.join(
        f'<a href="{r}{p or "./"}"{" aria-current=\"page\"" if current == p else ""}>{n}</a>' for n, p in NAV)
    links += f'<a href="{REPO}">{ICONS["GITHUB"]}GitHub</a>'
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{r or "./"}"><img src="{r}assets/icon-192.png" width="40" height="40" alt=""><span><b>Duo Clone</b><small>Developer page by XLAB</small></span></a>
    <nav class="nav" aria-label="Main">{links}</nav>
  </div>
</header>'''


def footer(depth: int) -> str:
    r = rel(depth)
    return f'''<footer class="site-foot">
  <div class="wrap">
    <p>© 2026 XLAB. Duo Clone is not affiliated with any app it can clone.</p>
    <nav aria-label="Footer">
      <a href="{r}notes/">Developer notes</a>
      <a href="{r}changelog/">Changelog</a>
      <a href="{APP_SITE}">duoclone.com</a>
      <a href="{APP_SITE}privacy/">Privacy</a>
      <a href="{REPO}">GitHub</a>
      <a href="https://xlabcompany.com/">XLAB</a>
    </nav>
  </div>
</footer>'''


SCRIPT = '''<script>
(function(){
  var d=document.documentElement;
  if(!matchMedia('(prefers-reduced-motion: reduce)').matches) d.classList.add('motion-ok');
  var p=document.querySelector('[data-print]');
  if(p&&'IntersectionObserver' in window){var o=new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){setTimeout(function(){p.classList.add('in')},120);o.disconnect();}})},{threshold:.4});o.observe(p);}else if(p){p.classList.add('in');}
  var links=[].slice.call(document.querySelectorAll('.toc > ol a'));
  if(links.length&&'IntersectionObserver' in window){
    var map={};links.forEach(function(a){map[a.hash.slice(1)]=a;});
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.remove('on')});var a=map[e.target.id];if(a)a.classList.add('on');}})},{rootMargin:'-20% 0px -70% 0px'});
    Object.keys(map).forEach(function(id){var h=document.getElementById(id);if(h)io.observe(h);});
  }
})();
</script>'''


def page(meta: dict, body: str, depth: int, graph: list, og: str, current: str, og_type='website') -> str:
    r = rel(depth)
    url = SITE + meta['path']
    title = meta['title']
    desc = meta['description']
    assert len(title) <= 60, (title, len(title))
    assert 120 <= len(desc) <= 160, (meta['source'], len(desc))
    og_url = SITE + 'og/' + og
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#fbfbf8">
<meta name="author" content="XLAB">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Duo Clone developer page">
<meta property="og:title" content="{html.escape(meta.get('ogTitle', title))}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(meta.get('ogAlt', title))}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{og_url}">
<link rel="icon" type="image/png" sizes="32x32" href="{r}assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="64x64" href="{r}assets/favicon-64.png">
<link rel="apple-touch-icon" href="{r}assets/apple-touch-icon.png">
<link rel="preload" href="{r}assets/fonts/bricolage-wght.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{r}assets/fonts/be-vietnam-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/style.css">
<link rel="sitemap" type="application/xml" href="{SITE}sitemap.xml">
{jsonld(graph)}
</head>
<body>
{header(depth, current)}
<main id="main">
{body}
</main>
{footer(depth)}
{SCRIPT}
</body>
</html>
'''


# ---------------------------------------------------------------- components

def note_card(n: dict, depth: int, variant: str = '', level: int = 3) -> str:
    r = rel(depth)
    cls = f'note-card {variant}'.strip()
    return f'''<article class="{cls}">
  <div class="cover"><img src="{r}{n['path']}{n['cover']}" width="1200" height="630" alt="{html.escape(n['coverAlt'])}" loading="lazy" decoding="async"></div>
  <div>
    <p class="meta"><time datetime="{n['published']}">{fmt_date(n['published'])}</time> · {n['readMinutes']} min read</p>
    <h{level}><a href="{r}{n['path']}">{html.escape(n['h1'])}</a></h{level}>
    <p>{html.escape(n['card'])}</p>
  </div>
</article>'''


def notes_grid(notes: list, depth: int, level: int = 3) -> str:
    variants = ['lead', '', '', 'wide']
    cards = [note_card(n, depth, variants[i] if i < 4 else '', level) for i, n in enumerate(notes)]
    return '<div class="notes-grid">\n' + '\n'.join(cards) + '\n</div>'


def release_strip(rel_: dict) -> str:
    items = ''.join(f'<li>{i}</li>' for i in rel_['items'][:3])
    return f'''<div class="release-strip sheet">
  <p class="ver">{rel_['version']}<small>Build {rel_['build']} · {rel_['date']}</small></p>
  <ul>{items}</ul>
  <a class="btn paper" href="changelog/#v{rel_['version'].replace('.', '-')}">All changes {ICONS['ARROW']}</a>
</div>'''


def toc(body: str) -> str:
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    heads = [(i, t) for i, t in heads if i != 'sources']
    items = ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in heads)
    return f'''<nav class="toc" aria-label="On this page">
  <p>On this page</p>
  <ol>{items}</ol>
  <details><summary>On this page</summary><ol>{items}</ol></details>
</nav>'''


# ---------------------------------------------------------------- pages

def build():
    pages = {p.stem: load_page(p) for p in sorted((ROOT / 'src/pages').glob('*.html'))}
    releases = json.loads((ROOT / 'src/releases.json').read_text())
    order = ['notes-require-secure-env', 'notes-how-app-copies-stay-separate', 'notes-android-15-16-app-cloners',
             'notes-microg-in-an-app-cloner']
    notes = [pages[k] for k in order]
    latest = releases[0]
    built = []

    # Notes
    for n in notes:
        depth = n['path'].count('/')
        words = word_count(n['body'])
        others = [o for o in notes if o is not n][:3]
        related = '<div class="notes-grid">' + ''.join(note_card(o, depth) for o in others) + '</div>'
        body = f'''<article>
<header class="art-head">
  <div class="wrap">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="../../">Home</a></li><li><a href="../">Developer notes</a></li><li aria-current="page">{html.escape(n['h1'].split(':')[0])}</li></ol></nav>
      <h1>{html.escape(n['h1'])}</h1>
      <p class="byline"><span>By <b><a href="https://xlabcompany.com/" rel="author">XLAB</a></b>, developer of Duo Clone</span><span class="dot"></span><time datetime="{n['published']}">{fmt_date(n['published'])}</time><span class="dot"></span><span>{n['readMinutes']} min read</span></p>
    </div>
    <figure class="art-cover">
      <img src="{n['cover']}" width="1200" height="630" alt="{html.escape(n['coverAlt'])}" fetchpriority="high">
      <figcaption>{html.escape(n['caption'])}</figcaption>
    </figure>
  </div>
</header>
<div class="art-body">
  <div class="wrap">
    {toc(n['body'])}
    <div class="prose">
{n['body']}
    </div>
  </div>
</div>
</article>
<section class="section related" aria-labelledby="related-title">
  <div class="wrap">
    <div class="section-head"><h2 id="related-title">More developer notes</h2><a class="more" href="../">All notes {ICONS['ARROW']}</a></div>
    {related}
  </div>
</section>'''
        slug = n['path'].strip('/').split('/')[-1]
        graph = [org(), website(), app(), {
            '@type': 'BlogPosting', '@id': SITE + n['path'] + '#article', 'headline': n['h1'],
            'description': n['description'], 'datePublished': n['published'], 'dateModified': n.get('modified', n['published']),
            'author': {'@id': ORG_ID}, 'publisher': {'@id': ORG_ID}, 'image': SITE + 'og/' + slug + '.png',
            'mainEntityOfPage': SITE + n['path'], 'isPartOf': {'@id': WEBSITE_ID}, 'about': {'@id': APP_ID},
            'inLanguage': 'en', 'wordCount': words},
            crumbs([('Home', ''), ('Developer notes', 'notes/'), (n['h1'], n['path'])])]
        n['ogAlt'] = n['coverAlt']
        write(n['path'], page(n, body, depth, graph, slug + '.png', 'notes/', 'article'))
        built.append((n['path'], n.get('modified', n['published']), words))

    # Notes index
    idx = {'path': 'notes/', 'source': 'generated', 'title': 'Duo Clone Developer Notes: How an App Cloner Works',
           'description': 'Developer notes from XLAB on how the Duo Clone app cloner works: Android platform rules, container limits, Google sign-in and what each Android release changed.'}
    body = f'''<section class="list-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="../">Home</a></li><li aria-current="page">Developer notes</li></ol></nav>
    <h1>Developer notes</h1>
    <p class="lede">How an Android app cloner works underneath, written by XLAB, the developer of Duo Clone. Each note answers one question, cites the Android and Google documentation it relies on, and says plainly where the limits are.</p>
  </div>
</section>
<section class="section" style="padding-top:2rem" aria-label="All notes">
  <div class="wrap">{notes_grid(notes, 1, level=2)}</div>
</section>'''
    graph = [org(), website(), app(), {
        '@type': 'CollectionPage', '@id': SITE + 'notes/#page', 'url': SITE + 'notes/', 'name': 'Developer notes',
        'isPartOf': {'@id': WEBSITE_ID}, 'about': {'@id': APP_ID}, 'inLanguage': 'en',
        'mainEntity': {'@type': 'ItemList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'url': SITE + n['path'], 'name': n['h1']} for i, n in enumerate(notes)]}},
        crumbs([('Home', ''), ('Developer notes', 'notes/')])]
    write('notes/', page(idx, body, 1, graph, 'notes.png', 'notes/'))
    built.append(('notes/', max(n['published'] for n in notes), 0))

    # Changelog
    rel_html = []
    for i, r_ in enumerate(releases):
        vid = 'v' + r_['version'].replace('.', '-')
        items = ''.join(f'<li>{x}</li>' for x in r_['items'])
        rel_html.append(f'''<section class="release sheet" aria-labelledby="{vid}">
  <p class="v">{r_['version']}<small>Build {r_['build']}<br>{r_['date']}</small></p>
  <div><h2 id="{vid}">Version {r_['version']} (build {r_['build']})</h2><ul>{items}</ul></div>
</section>''')
    cl = {'path': 'changelog/', 'source': 'generated',
          'title': f'Duo Clone Changelog – Release Notes {releases[-1]["version"]} to {latest["version"]}',
          'description': f'Release notes for Duo Clone versions {releases[-1]["version"]} to {latest["version"]}: new color theme and icon, fixes for typing, browsers, camera and permission notices in clones.'}
    body = f'''<section class="list-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="../">Home</a></li><li aria-current="page">Changelog</li></ol></nav>
    <h1>Changelog</h1>
    <p class="lede">What changed in each version of Duo Clone, newest first. Dates are in GMT+7. For the reasoning behind some of these fixes, read the <a href="../notes/android-15-16-app-cloners/">note on Android 15 and 16</a>.</p>
  </div>
</section>
<section class="section" style="padding-top:2rem" aria-label="Releases">
  <div class="wrap"><div class="releases">{''.join(rel_html)}</div>
  <p style="margin-top:2.5rem">Questions or bug reports? <a href="{REPO}/issues">Open an issue on GitHub</a>.</p></div>
</section>'''
    graph = [org(), website(), app(), {'@type': 'WebPage', '@id': SITE + 'changelog/#page', 'url': SITE + 'changelog/',
             'name': 'Duo Clone changelog', 'isPartOf': {'@id': WEBSITE_ID}, 'about': {'@id': APP_ID}, 'inLanguage': 'en',
             'dateModified': '2026-11-20'}, crumbs([('Home', ''), ('Changelog', 'changelog/')])]
    write('changelog/', page(cl, body, 1, graph, 'changelog.png', 'changelog/'))
    built.append(('changelog/', '2026-11-20', 0))

    # Home
    home = pages['home']
    body = fill_tokens(home['body'], {'NOTES_GRID': notes_grid(notes, 0), 'RELEASE_STRIP': release_strip(latest),
                                      'LATEST_VERSION': latest['version']})
    graph = [org(), website(), app(), {'@type': 'WebPage', '@id': SITE + '#page', 'url': SITE, 'name': home['title'],
             'isPartOf': {'@id': WEBSITE_ID}, 'about': {'@id': APP_ID}, 'primaryImageOfPage': SITE + 'assets/icon-512.png',
             'inLanguage': 'en', 'dateModified': '2026-11-20'}]
    home['ogAlt'] = 'Duo Clone app icon printed in green and pink on paper, with the words Duo Clone developer page'
    write('', page(home, body, 0, graph, 'home.png', ''))
    built.append(('', '2026-11-20', 0))

    # 404
    nf = {'path': '404.html', 'source': 'generated', 'title': 'Page not found – Duo Clone developer page',
          'description': 'This page does not exist on the Duo Clone developer page. Go back to the home page, the developer notes or the changelog to find what you need.'}
    body = f'''<section class="list-head" style="padding-bottom:5rem"><div class="wrap">
<h1>Page not found</h1><p class="lede">This address does not exist on the Duo Clone developer page.</p>
<p style="margin-top:2rem;display:flex;gap:1rem;flex-wrap:wrap"><a class="btn" href="{SITE}">Home</a><a class="btn paper" href="{SITE}notes/">Developer notes</a></p></div></section>'''
    out = page(nf, body, 0, [org(), website()], 'home.png', '').replace('href="assets/', f'href="{SITE}assets/').replace('src="assets/', f'src="{SITE}assets/')
    out = out.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    out = out.replace(f'<link rel="canonical" href="{SITE}404.html">\n', '')
    (DOCS / '404.html').write_text(out)

    # sitemap + robots
    urls = ''.join(f'  <url><loc>{SITE}{p}</loc><lastmod>{m}</lastmod></url>\n' for p, m, _ in sorted(built))
    (DOCS / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    (DOCS / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n')
    for p, _, w in built:
        if w:
            print(f'{p:45} {w} words')


def write(path: str, text: str):
    out = DOCS / path / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)


if __name__ == '__main__':
    build()
