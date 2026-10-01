#!/usr/bin/env python3
"""Modernize huntsvillehvacpros.com page markup (2026-10-01).

Pairs with docs/css/modern.css. Keeps every word, heading, link, phone number, JSON-LD block,
meta tag, form and analytics script; changes presentation only:
  - loads Outfit + Inter and css/modern.css LAST, versions the existing sheets (?v=20261001)
  - body gets class "hv hv-<kind>" so every modern rule is scoped
  - inner-page heroes get a real repo photo (--hero-img), location breadcrumbs move into the hero
  - star glyphs (&#9733;) become solid SVG stars (emoji rule)
  - FAQ accordions become native <details> (work without JS)
  - section backgrounds that were inline styles become band classes with real light/dark rhythm
  - home PAS blocks get classes (split intro with photo, icon cards, price cards, climate cards)
  - blog index gradient placeholders become photo thumbnails
  - mid-page CTA wrapper loses its inline padding (it produced 280-300px dead bands)
Idempotent: a page already carrying body class "hv" is skipped.
Never touches /job/, /lead/, /leads/, /estimate/.

usage: python3 modernize-huntsville.py <docs-root>
"""
import re, sys, glob, os

ROOT = sys.argv[1]
ICONS = '/private/tmp/claude-501/-Users-costademetral-RankAndRent/8bd723fd-372d-4cb0-889c-0aa1e748e063/scratchpad/c/icons/package/20/solid'
V = '20261001'


def icon(name, cls='hv-i'):
    svg = open(os.path.join(ICONS, name + '.svg')).read().strip()
    svg = re.sub(r'\s*data-slot="icon"', '', svg)
    svg = re.sub(r'\s*\n\s*', ' ', svg)
    return svg.replace('<svg ', f'<svg class="{cls}" ', 1)


STAR = icon('star', 'hv-star')
STARS5 = '<span class="hv-stars" role="img" aria-label="5 out of 5 stars">' + STAR * 5 + '</span>'

HERO_IMG = {
    'services/ac-repair.html': 'hero-ac-repair.webp',
    'services/ac-installation.html': 'hero-ac-installation.webp',
    'services/emergency.html': 'hero-emergency.webp',
    'services/heating.html': 'hero-heating.webp',
    'services/maintenance.html': 'hero-maintenance.webp',
    'services/index.html': 'hero-main.webp',
    'locations/meridianville.html': 'service-ac-unit.webp',
    'blog/index.html': 'hero-maintenance.webp',
    'blog/signs-ac-needs-repair.html': 'blog-signs-repair.webp',
    'blog/summer-ac-prep-huntsville.html': 'blog-summer-prep.webp',
    'blog/choosing-hvac-system-huntsville.html': 'blog-hvac-choice.webp',
    'blog/ac-running-but-not-cooling.html': 'hero-ac-repair.webp',
    'blog/how-long-does-ac-unit-last.html': 'ba-before-ac.jpg',
    'blog/how-much-does-hvac-cost-huntsville.html': 'hero-ac-installation.webp',
    'about.html': 'about-team.webp',
    'faq.html': 'hero-heating.webp',
    'contact.html': 'hero-emergency.webp',
    'privacy.html': 'hero-main.webp',
    'thank-you.html': 'hero-main.webp',
}
BLOG_THUMB = {
    'signs-ac-needs-repair': 'blog-signs-repair.webp',
    'summer-ac-prep-huntsville': 'blog-summer-prep.webp',
    'choosing-hvac-system-huntsville': 'blog-hvac-choice.webp',
    'how-much-does-hvac-cost-huntsville': 'hero-ac-installation.webp',
    'ac-running-but-not-cooling': 'hero-ac-repair.webp',
    'how-long-does-ac-unit-last': 'ba-before-ac.jpg',
}


def kind_of(rel):
    if rel == 'index.html': return 'home'
    if rel.startswith('services/'): return 'hub' if rel.endswith('index.html') else 'svc'
    if rel.startswith('locations/'): return 'loc'
    if rel.startswith('blog/'): return 'blogidx' if rel.endswith('index.html') else 'post'
    return 'page'


def hero_img(rel):
    if rel in HERO_IMG: return HERO_IMG[rel]
    if rel.startswith('locations/'):
        slug = os.path.basename(rel)[:-5]
        if os.path.exists(os.path.join(ROOT, 'images', f'loc-{slug}.webp')): return f'loc-{slug}.webp'
    return 'hero-main.webp'


def faq_to_details(body):
    # <div class="faq__item"><button class="faq__question">Q<icon/></button><div class="faq__answer">A</div></div>
    pat = re.compile(
        r'<div class="faq__item">\s*<button class="faq__question">\s*(.*?)\s*<(span|div) class="faq__icon">.*?</\2>\s*</button>\s*'
        r'<div class="faq__answer">\s*(<div class="faq__answer-inner">.*?</div>|(?:(?!<div).)*?)\s*</div>\s*</div>', re.S)
    plus = '<span class="faq__icon hv-faq-icon" aria-hidden="true"></span>'
    def rep(m):
        return (f'<details class="faq__item hv-faq"><summary class="faq__question">{m.group(1)}{plus}</summary>'
                f'<div class="faq__answer">{m.group(3)}</div></details>')
    return pat.sub(rep, body)


def assign_bands(body):
    """Give every content <section> a band class; strip inline background so the class decides."""
    tags = list(re.finditer(r'<section\b[^>]*>', body))
    info = []
    for m in tags:
        t = m.group(0)
        cls = re.search(r'class="([^"]*)"', t)
        cls = cls.group(1) if cls else ''
        style = re.search(r'style="([^"]*)"', t)
        style = style.group(1) if style else ''
        if re.search(r'\b(hero|trust-bar|cta-section)\b', cls):
            info.append(None); continue
        if re.search(r'\b(process|testimonials)\b', cls):
            info.append('dark'); continue
        if 'color-primary' in style:
            info.append('dark?'); continue
        info.append('light')
    # resolve optional dark: dark only if neither neighbour is dark
    resolved = []
    for i, b in enumerate(info):
        if b == 'dark?':
            prev = resolved[-1] if resolved else None
            nxt = info[i + 1] if i + 1 < len(info) else None
            b = 'dark' if prev != 'dark' and nxt not in ('dark',) else 'light'
        resolved.append(b)
    out, last, alt = [], 0, 0
    for m, b in zip(tags, resolved):
        t = m.group(0)
        if b is None:
            new = t
        else:
            if b == 'dark':
                band = 'hv-band hv-band--dark'; alt = 0
            else:
                band = 'hv-band' + (' hv-band--soft' if alt % 2 else ''); alt += 1
            new = re.sub(r'style="([^"]*)"', lambda s: (lambda r: f'style="{r}"' if r.strip(' ;') else '')(
                re.sub(r'background:[^;"]*;?', '', s.group(1))), t)
            new = re.sub(r'\s+>', '>', new.replace(' style=""', ''))
            new = new.replace('class="', f'class="{band} ', 1) if 'class="' in new else new.replace('<section', f'<section class="{band}"', 1)
        out.append(body[last:m.start()] + new); last = m.end()
    out.append(body[last:])
    return ''.join(out)


def strip_styles(fragment):
    return re.sub(r'\s+style="[^"]*"', '', fragment)


def home_pas(body):
    """Home page PAS blocks: inline-styled text walls -> classed layouts."""
    secs = list(re.finditer(r'<section class="page-section" style="[^"]*">(.*?)</section>', body, re.S))
    badges_agitate = ['fire', 'cloud', 'wrench-screwdriver', 'clock']
    badges_climate = ['sun', 'cloud', 'beaker']
    for m in reversed(secs):
        inner = m.group(1)
        if 'Worst Possible Time' in inner:
            inner = strip_styles(inner)
            inner = re.sub(r'^\s*<div>', '<div class="container hv-split"><div class="hv-split__copy">', inner, count=1)
            inner = re.sub(r'</div>\s*$', '</div><figure class="hv-split__media"><img src="/images/hero-ac-repair.webp" alt="Technician servicing an outdoor AC condenser in Huntsville" loading="lazy" width="900" height="600"><figcaption>Same-day diagnosis across Huntsville and Madison County</figcaption></figure></div>', inner, count=1)
            cls = 'page-section hv-pas hv-pas--problem'
        elif 'Every Hour Without AC' in inner:
            inner = strip_styles(inner)
            inner = re.sub(r'^\s*<div>', '<div class="container hv-narrow-wide">', inner, count=1)
            inner = inner.replace('<ul>', '<ul class="hv-cards hv-cards--2">', 1)
            i = iter(badges_agitate)
            inner = re.sub(r'<li>', lambda _: f'<li class="hv-card"><span class="hv-badge">{icon(next(i))}</span>', inner)
            cls = 'page-section hv-pas hv-pas--agitate'
        elif 'What Does HVAC Service Cost' in inner:
            inner = strip_styles(inner)
            inner = re.sub(r'^\s*<div>', '<div class="container hv-narrow-wide">', inner, count=1)
            inner = re.sub(r'<div>\s*<div>(Diagnostic Service Call|Common Repairs|System Replacement)</div>\s*<div>',
                           r'<div class="hv-card hv-price"><div class="hv-price__name">\1</div><div class="hv-price__body">', inner)
            inner = inner.replace('<div class="hv-price__name">Diagnostic Service Call</div><div class="hv-price__body">',
                                  '<div class="hv-price__name">Diagnostic Service Call</div><div class="hv-price__amt">', 1)
            inner = re.sub(r'(<div class="hv-price__amt">[^<]*</div>\s*)<div>', r'\1<div class="hv-price__body">', inner, count=1)
            inner = re.sub(r'(</p>\s*)<div>(\s*<div class="hv-card)', r'\1<div class="hv-cards hv-cards--3 hv-prices">\2', inner, count=1)
            cls = 'page-section hv-pas hv-pas--price'
        elif 'Climate Demands' in inner:
            inner = strip_styles(inner)
            inner = re.sub(r'^\s*<div>', '<div class="container hv-narrow-wide">', inner, count=1)
            inner = re.sub(r'(</p>\s*)<div>', r'\1<div class="hv-cards hv-cards--3">', inner, count=1)
            i = iter(badges_climate)
            inner = re.sub(r'<div>(\s*<strong>)', lambda mm: f'<div class="hv-card"><span class="hv-badge">{icon(next(i))}</span>{mm.group(1)}', inner)
            cls = 'page-section hv-pas hv-pas--climate'
        else:
            continue
        body = body[:m.start()] + f'<section class="{cls}">' + inner + '</section>' + body[m.end():]
    return body


def transform(path):
    html = open(path, encoding='utf-8').read()
    if re.search(r'<body[^>]*class="[^"]*\bhv\b', html): return 'skip (already modern)'
    rel = os.path.relpath(path, ROOT)
    kind = kind_of(rel)

    # stylesheets: version the old pair, add fonts + modern.css last
    html = re.sub(r'(href="/?css/style\.v2\.5\.css)(\?v=[^"]*)?"', rf'\1?v={V}"', html)
    html = re.sub(r'(href="/?css/site-theme\.css)(\?v=[^"]*)?"', rf'\1?v={V}"', html)
    if 'css/style.v2.5.css' not in html:
        return 'skip (not a template page)'
    head_add = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap">'
                f'<link rel="stylesheet" href="/css/modern.css?v={V}">\n</head>')
    html = html.replace('</head>', head_add, 1)
    html = re.sub(r'<body([^>]*)>', lambda m: f'<body{m.group(1)} class="hv hv-{kind}">' if 'class=' not in m.group(1)
                  else '<body' + m.group(1).replace('class="', f'class="hv hv-{kind} ') + '>', html, count=1)

    head, body = html.split('<body', 1)

    # inner hero photo
    if kind != 'home':
        img = hero_img(rel)
        body = body.replace('<section class="hero hero--inner">', f'<section class="hero hero--inner" style="--hero-img:url(/images/{img})">', 1)

    # location breadcrumb: move from the strip under the hero to the top of the hero copy
    bc = re.search(r'\s*(?:<!-- ===== BREADCRUMB ===== -->\s*)?<div class="breadcrumb">\s*<div class="container breadcrumb__inner">(.*?)</div>\s*</div>', body, re.S)
    if bc and 'hero__content' in body:
        crumbs = bc.group(1).strip()
        body = body[:bc.start()] + body[bc.end():]
        body = re.sub(r'(<div class="hero__content"[^>]*>)', lambda m: m.group(1) + f'<nav class="breadcrumb__inner hv-crumbs" aria-label="Breadcrumb">{crumbs}</nav>', body, count=1)

    # location pages: a price list that lost its markup renders as one run-on line; restore rows (same words)
    def pricelist(m):
        rows = re.findall(r'(.+?:)(\$[\d,]+\u2013\$[\d,]+)(?: (\([^)]*\)))?', m.group(1))
        if ''.join(a + b + (' ' + c if c else '') for a, b, c in rows) != m.group(1): return m.group(0)
        return '<div class="hv-pricelist">' + ''.join(
            f'<div class="pricing-row"><span class="pricing-row__label">{a}' + (f' <small>{c}</small>' if c else '') +
            f'</span><span class="pricing-row__price">{b}</span></div>' for a, b, c in rows) + '</div>'
    body = re.sub(r'<p style="[^"]*">(Service call \+ diagnostic:[^<]*)</p>', pricelist, body)

    # star glyphs -> solid svg
    body = re.sub(r'(?:&#9733;|★){5}', STARS5, body)

    # FAQ -> native accordion
    body = faq_to_details(body)

    # home-only PAS blocks
    if kind == 'home':
        body = home_pas(body)

    # bands
    body = assign_bands(body)

    # mid-page CTA wrapper on service pages: inline bottom padding produced a dead band
    body = body.replace('<div class="container" style="padding:0 1.5rem 5rem;">', '<div class="container hv-midcta">')

    # blog index: gradient placeholder -> photo thumbnail
    if kind == 'blogidx':
        def thumb(m):
            slug = m.group(1)
            img = BLOG_THUMB.get(slug, 'hero-main.webp')
            return (f'<a href="/blog/{slug}.html" class="bento__card hv-post-card reveal" style="text-decoration:none;">'
                    f'<div class="hv-thumb"><img src="/images/{img}" alt="" loading="lazy" width="600" height="400"></div>')
        body = re.sub(r'<a href="/blog/([a-z0-9-]+)\.html" class="bento__card reveal" style="text-decoration:none;">\s*<div style="height:200px;[^"]*">.*?</svg></div></div>',
                      thumb, body, flags=re.S)

    # hub page cards: inline dark backgrounds on a light band -> let modern.css style them
    if kind == 'hub':
        body = re.sub(r'(<a href="/services/[a-z-]+\.html" class="why__stat-card) reveal" style="[^"]*">',
                      r'\1 hv-svc-card reveal">', body)
        body = re.sub(r'(<a href="/services/[a-z-]+\.html" class="why__stat-card hv-svc-card reveal">\s*)<div style="[^"]*">',
                      r'\1<div class="hv-badge">', body)
        body = re.sub(r'(<div class="hv-badge">.*?</div>\s*)<h3 style="[^"]*">', r'\1<h3>', body, flags=re.S)
        body = re.sub(r'(<a href="/services/[a-z-]+\.html" class="why__stat-card hv-svc-card reveal">(?:(?!</a>).)*?)<p style="[^"]*">', r'\1<p>', body, flags=re.S)
        body = re.sub(r'(<a href="/services/[a-z-]+\.html" class="why__stat-card hv-svc-card reveal">(?:(?!</a>).)*?)<span style="[^"]*">', r'\1<span class="hv-more">', body, flags=re.S)

    left = re.findall('[\U0001F000-\U0001FAFF☀-➿⬀-⯿]', body)
    if left: raise SystemExit(f'{rel}: emoji left {set(left)}')
    open(path, 'w', encoding='utf-8').write(head + '<body' + body)
    return f'ok ({kind})'


for f in sorted(glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith(('lead/', 'leads/', 'job/', 'estimate/')) or rel.startswith('_'): continue
    print(rel, transform(f))
