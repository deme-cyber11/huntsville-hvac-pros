#!/usr/bin/env python3
"""
Rebuild svc-content / loc-content sections with proper v2.5 alternating section structure.
Run from the site root: python3 rebuild-content-sections.py
"""
import re, sys
from pathlib import Path
from bs4 import BeautifulSoup

DOCS = Path("/Users/costa.demetral/Documents/Rank and Rent $/My-RR-Sites/Huntsville-HVAC-Pros/docs")

# ─── SHARED COMPONENTS ────────────────────────────────────────────────────────
def stat_cards(items):
    """items: list of (emoji, title, desc)"""
    cards = "\n".join(
        f'<div class="why__stat-card reveal"><div style="font-size:2rem;margin-bottom:.5rem;">{e}</div><strong>{t}</strong><p>{d}</p></div>'
        for e, t, d in items
    )
    return f'<div class="why__stats" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.5rem;margin-top:3rem;">\n{cards}\n</div>'

def ul_to_cards(items_html):
    """Convert <li> items to why__stat-card grid. items_html: list of (strong_text, rest_text)"""
    cards = "\n".join(
        f'<div class="why__stat-card reveal"><h3>{t}</h3><p>{d}</p></div>'
        for t, d in items_html
    )
    return f'<div class="why__stats" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.5rem;margin-top:2rem;">\n{cards}\n</div>'

def checklist_items(items):
    rows = "\n".join(
        f'<div style="display:flex;gap:1rem;align-items:flex-start;"><span style="color:var(--color-accent);font-size:1.25rem;flex-shrink:0;margin-top:.1rem;">✓</span>'
        f'<div><strong style="color:var(--color-dark);">{t}</strong><p style="color:var(--color-text-light);font-size:.9375rem;margin:.25rem 0 0;">{d}</p></div></div>'
        for t, d in items
    )
    return f'<div style="display:flex;flex-direction:column;gap:1.25rem;">\n{rows}\n</div>'

def pricing_rows(items):
    rows = "\n".join(
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding:1rem 1.25rem;background:var(--color-surface);border-radius:8px;border-left:3px solid var(--color-accent);">'
        f'<span style="font-weight:600;color:var(--color-dark);">{label}</span>'
        f'<span style="color:var(--color-accent);font-weight:700;">{price}</span></div>'
        for label, price in items
    )
    return f'<div style="display:flex;flex-direction:column;gap:.75rem;">\n{rows}\n</div>'

def process_cards(steps):
    """steps: list of (title, desc)"""
    icons = [
        '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>',
        '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
        '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
        '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
        '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>',
    ]
    cards = "\n".join(
        f'<div class="process__card reveal"><div class="process__num">{i+1}</div>'
        f'<div class="process__icon">{icons[i % len(icons)]}</div>'
        f'<h3 class="process__card-title">{t}</h3>'
        f'<p class="process__card-desc">{d}</p></div>'
        for i, (t, d) in enumerate(steps)
    )
    return f'<div class="process__grid">\n{cards}\n</div>'

def cta_box(headline, subline, primary_text="Call (256) 215-9287", primary_href="tel:+12562159287"):
    return f'''\
<div class="container" style="padding:0 1.5rem 5rem;">
  <div class="svc-cta-box reveal">
    <h2>{headline}</h2>
    <p>{subline}</p>
    <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
      <a href="{primary_href}" class="btn btn--primary">{primary_text}</a>
      <a href="/contact.html" class="btn btn--outline" style="border-color:rgba(255,255,255,0.4);color:white;">Schedule Online</a>
    </div>
  </div>
</div>'''

def service_link_cards(services):
    """services: list of (href, title, desc)"""
    cards = "\n".join(
        f'<a href="{href}" class="why__stat-card reveal" style="text-decoration:none;display:block;">'
        f'<h3>{t}</h3><p>{d}</p>'
        f'<span style="color:var(--color-accent);font-weight:700;font-size:.875rem;">Learn More →</span></a>'
        for href, t, d in services
    )
    return f'<div class="why__stats" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.5rem;margin-top:3rem;">\n{cards}\n</div>'

SVC_LINKS = [
    ("/services/ac-repair.html", "AC Repair", "Same-day AC repair. Written quote before we touch anything."),
    ("/services/ac-installation.html", "AC Installation", "New systems sized right. All major brands available."),
    ("/services/heating.html", "Heating Services", "Gas furnace and heat pump repair, installation, and maintenance."),
    ("/services/maintenance.html", "Maintenance Plans", "Twice-yearly tune-ups. Catch problems before emergencies."),
    ("/services/emergency.html", "Emergency HVAC", "24/7 emergency response. We target 2–4 hours."),
]


# ─── PARSE HELPERS ────────────────────────────────────────────────────────────
def parse_li_items(ul_el):
    """Extract (strong_text, rest_text) from <li><strong>...</strong>...</li>"""
    items = []
    for li in ul_el.find_all('li'):
        strong = li.find('strong')
        if strong:
            title = strong.get_text(strip=True).rstrip('.')
            rest = li.get_text(separator=' ', strip=True)
            rest = rest.replace(strong.get_text(strip=True), '', 1).strip().lstrip('-–—').strip()
        else:
            full = li.get_text(strip=True)
            title = full.split('.')[0].strip() if '.' in full else full[:50]
            rest = full
        items.append((title, rest))
    return items

def parse_ol_steps(ol_el):
    """Extract (title, desc) from <li><strong>Title</strong> desc</li>"""
    steps = []
    for li in ol_el.find_all('li'):
        strong = li.find('strong')
        if strong:
            title = strong.get_text(strip=True).rstrip('.')
            rest = li.get_text(separator=' ', strip=True)
            rest = rest.replace(strong.get_text(strip=True), '', 1).strip().lstrip('.').strip()
        else:
            full = li.get_text(strip=True)
            title = full.split('.')[0]
            rest = full
        steps.append((title, rest))
    return steps

def get_paragraphs_html(el):
    """Get all <p> text from an element as list of strings."""
    return [p.get_text(strip=True) for p in el.find_all('p', recursive=False) if p.get_text(strip=True)]

def paras_to_html(paras):
    return "\n".join(f'<p class="why__text">{p}</p>' for p in paras)

def section_h2_map(soup_section):
    """Return ordered list of (h2_text, content_el_list) from a section."""
    results = []
    current_h2 = None
    current_els = []
    for el in soup_section.find('div', class_='container').children:
        if el.name == 'h2':
            if current_h2 is not None:
                results.append((current_h2, current_els))
            current_h2 = el.get_text(strip=True)
            current_els = []
        elif el.name in ['p', 'ul', 'ol', 'div'] and current_h2:
            current_els.append(el)
    if current_h2:
        results.append((current_h2, current_els))
    return results


# ─── SERVICE PAGE REBUILD ──────────────────────────────────────────────────────
def rebuild_svc_content(html, page_meta):
    soup = BeautifulSoup(html, 'lxml')
    svc = soup.find('section', class_='svc-content')
    if not svc:
        print(f"  ⚠️  No svc-content found")
        return html

    sections = section_h2_map(svc)
    print(f"  Found {len(sections)} h2 sections: {[s[0][:40] for s in sections]}")

    m = page_meta
    new_html = []

    # Section 1: Intro (white) — first h2 + paras + stat cards
    if sections:
        h2_text, els = sections[0]
        paras = [el.get_text(strip=True) for el in els if el.name == 'p']
        new_html.append(f'''
<section class="why" style="background:var(--color-white);">
  <div class="container">
    <div class="why__inner">
      <div class="why__content reveal">
        <span class="section-label">{m["badge"]}</span>
        <h2 class="section-title">{h2_text}</h2>
        {paras_to_html(paras[:3])}
        <a href="tel:+12562159287" class="btn btn--primary" style="margin-top:1.5rem;">Call (256) 215-9287 Now</a>
      </div>
      {stat_cards(m["intro_cards"])}
    </div>
  </div>
</section>''')

    # Section 2: Core service grid (dark) — second h2, ul items → cards
    for h2_text, els in sections[1:3]:
        ul_el = next((e for e in els if e.name in ['ul', 'ol']), None)
        paras = [el.get_text(strip=True) for el in els if el.name == 'p']
        if ul_el and ul_el.name == 'ul':
            items = parse_li_items(ul_el)
            grid = ul_to_cards(items[:6])
        elif ul_el and ul_el.name == 'ol':
            steps = parse_ol_steps(ul_el)
            # Render as process section
            new_html.append(f'''
<section class="process">
  <div class="container">
    <div class="process__header reveal">
      <span class="section-label section-label--light">How It Works</span>
      <h2 class="section-title">{h2_text}</h2>
      <p class="section-subtitle">{paras[0] if paras else "Step by step, from your call to a working system."}</p>
    </div>
    {process_cards(steps[:5])}
  </div>
</section>''')
            continue
        else:
            grid = paras_to_html(paras)

        new_html.append(f'''
<section class="why">
  <div class="container">
    <div class="why__header reveal">
      <h2 class="section-title">{h2_text}</h2>
      {"<p class='section-subtitle'>" + paras[0] + "</p>" if paras else ""}
    </div>
    {grid}
  </div>
</section>''')

    # Remaining sections: process if ol, white 2-col for pairs, else single white
    remaining = sections[3:]
    i = 0
    while i < len(remaining):
        h2_text, els = remaining[i]
        ul_el = next((e for e in els if e.name in ['ul', 'ol']), None)
        paras = [el.get_text(strip=True) for el in els if el.name == 'p']
        text_paras = "\n".join(f'<p style="color:var(--color-text-light);line-height:1.8;margin-bottom:1rem;">{p}</p>' for p in paras)

        # Check for process/ol
        if ul_el and ul_el.name == 'ol':
            steps = parse_ol_steps(ul_el)
            new_html.append(f'''
<section class="process">
  <div class="container">
    <div class="process__header reveal">
      <span class="section-label section-label--light">How It Works</span>
      <h2 class="section-title">{h2_text}</h2>
      <p class="section-subtitle">{paras[0] if paras else ""}</p>
    </div>
    {process_cards(steps[:5])}
  </div>
</section>''')
            i += 1
            continue

        # Check for pricing/cost section
        h2_low = h2_text.lower()
        if any(k in h2_low for k in ['cost', 'pric', 'rate', 'financ', 'fee']):
            # Pair with previous checklist if available
            if ul_el and ul_el.name == 'ul':
                items = parse_li_items(ul_el)
                # render as price rows if items look like price ranges
                any_dollar = any('$' in t + d for t, d in items)
                if any_dollar:
                    price_items = [(t, d.split('$')[-1].strip() if '$' in d else d[:30]) for t, d in items]
                    rows_html = pricing_rows([(t, f"${p}" if not p.startswith('$') else p) for t, p in price_items])
                else:
                    rows_html = ul_to_cards(items)
                new_html.append(f'''
<section class="why" style="background:var(--color-white);">
  <div class="container">
    <div class="why__header reveal">
      <h2 class="section-title">{h2_text}</h2>
      {"<p class='section-subtitle'>" + paras[0] + "</p>" if paras else ""}
    </div>
    <div style="max-width:600px;margin:2rem auto 0;" class="reveal">
      {rows_html}
      {"<p style='color:var(--color-text-light);font-size:.875rem;margin-top:1rem;'>" + paras[-1] + "</p>" if len(paras) > 1 else ""}
    </div>
  </div>
</section>''')
            else:
                new_html.append(f'''
<section class="why" style="background:var(--color-white);">
  <div class="container">
    <div class="why__inner reveal">
      <div class="why__content">
        <h2 class="section-title">{h2_text}</h2>
        {text_paras}
      </div>
    </div>
  </div>
</section>''')
            i += 1
            continue

        # Two consecutive sections → 2-col white layout
        if i + 1 < len(remaining):
            h2b, elsb = remaining[i + 1]
            ulb = next((e for e in elsb if e.name in ['ul', 'ol']), None)
            parasb = [el.get_text(strip=True) for el in elsb if el.name == 'p']
            text_parasb = "\n".join(f'<p style="color:var(--color-text-light);line-height:1.8;margin-bottom:.75rem;">{p}</p>' for p in parasb)

            def arrow_list(ul):
                if not ul: return ""
                return "<div style='display:flex;flex-direction:column;gap:.5rem;margin-top:.75rem;'>" + "".join(
                    f"<div style='display:flex;gap:.75rem;'><span style='color:var(--color-accent);font-weight:700;flex-shrink:0;'>→</span><span style='color:var(--color-text-light);'>{li.get_text(strip=True)}</span></div>"
                    for li in ul.find_all('li')
                ) + "</div>"

            new_html.append(f'''
<section class="why" style="background:var(--color-white);">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:start;" class="reveal">
      <div>
        <h2 class="section-title" style="margin-bottom:1.5rem;">{h2_text}</h2>
        {text_paras}
        {arrow_list(ul_el)}
      </div>
      <div>
        <h2 class="section-title" style="margin-bottom:1.5rem;">{h2b}</h2>
        {text_parasb}
        {arrow_list(ulb)}
      </div>
    </div>
  </div>
</section>''')
            i += 2
            continue

        # Single remaining section — white with ul as checklist or card grid
        if ul_el and ul_el.name == 'ul':
            items = parse_li_items(ul_el)
            grid = ul_to_cards(items)
        else:
            grid = text_paras

        new_html.append(f'''
<section class="why" style="background:var(--color-white);">
  <div class="container">
    <div class="why__header reveal">
      <h2 class="section-title">{h2_text}</h2>
      {"<p class='section-subtitle'>" + paras[0] + "</p>" if paras else ""}
    </div>
    {grid}
  </div>
</section>''')
        i += 1

    # Mid-page CTA
    new_html.append(cta_box(m['cta_h'], m['cta_p']))

    new_section = "\n".join(new_html)

    # Replace old svc-content in html string
    result = re.sub(
        r'<section class="svc-content">.*?</section>(?=\s*<!--)',
        new_section,
        html,
        flags=re.DOTALL
    )
    if result == html:
        result = re.sub(
            r'<section class="svc-content">.*?</section>',
            new_section,
            html,
            flags=re.DOTALL,
            count=1
        )
    return result


# ─── LOCATION PAGE REBUILD ─────────────────────────────────────────────────────
def rebuild_loc_content(html, city_meta):
    soup = BeautifulSoup(html, 'lxml')
    loc = soup.find('section', class_='loc-content')
    if not loc:
        print(f"  ⚠️  No loc-content found")
        return html

    sections = section_h2_map(loc)
    print(f"  Found {len(sections)} h2 sections")

    m = city_meta
    new_html = []

    # Section 1: Intro (white) + stat cards
    h2_text, els = sections[0]
    paras = [el.get_text(strip=True) for el in els if el.name == 'p']
    new_html.append(f'''
<section class="why" style="background:var(--color-white);">
  <div class="container">
    <div class="why__inner">
      <div class="why__content reveal">
        <span class="section-label">HVAC Service in {m["city"]}, AL</span>
        <h2 class="section-title">{h2_text}</h2>
        {paras_to_html(paras[:2])}
        <a href="tel:+12562159287" class="btn btn--primary" style="margin-top:1.5rem;">Call (256) 215-9287</a>
      </div>
      {stat_cards(m["intro_cards"])}
    </div>
  </div>
</section>''')

    # Section 2: Neighborhoods (dark grid) — if present
    nb_section = next((s for s in sections if any(k in s[0].lower() for k in ['neighborhood', 'area', 'communit', 'surround'])), None)
    if nb_section:
        h2n, elsn = nb_section
        ul_el = next((e for e in elsn if e.name == 'ul'), None)
        if ul_el:
            items = parse_li_items(ul_el)
            grid = ul_to_cards(items)
        else:
            grid = paras_to_html([el.get_text(strip=True) for el in elsn if el.name == 'p'])
        new_html.append(f'''
<section class="why">
  <div class="container">
    <div class="why__header reveal">
      <h2 class="section-title">{h2n}</h2>
      <p class="section-subtitle">Every neighborhood in {m["city"]} has different HVAC demands. We know them all.</p>
    </div>
    {grid}
  </div>
</section>''')

    # Middle sections (city-specific): pair into 2-col or single white sections
    skip_keys = ['neighborhood', 'area we serve', 'communit', 'service available', 'hvac service available']
    middle = [s for s in sections[1:] if not any(k in s[0].lower() for k in skip_keys + ['service available'])]
    i = 0
    while i < len(middle):
        h2a, elsa = middle[i]
        parasa = [el.get_text(strip=True) for el in elsa if el.name == 'p']
        ula = next((e for e in elsa if e.name == 'ul'), None)
        text_a = "\n".join(f'<p style="color:var(--color-text-light);line-height:1.8;margin-bottom:.75rem;">{p}</p>' for p in parasa)
        arrows_a = ""
        if ula:
            arrows_a = "<div style='display:flex;flex-direction:column;gap:.5rem;margin-top:.75rem;'>" + "".join(
                f"<div style='display:flex;gap:.75rem;'><span style='color:var(--color-accent);font-weight:700;flex-shrink:0;'>→</span><span style='color:var(--color-text-light);'>{li.get_text(strip=True)}</span></div>"
                for li in ula.find_all('li')
            ) + "</div>"

        if i + 1 < len(middle):
            h2b, elsb = middle[i + 1]
            parasb = [el.get_text(strip=True) for el in elsb if el.name == 'p']
            ulb = next((e for e in elsb if e.name == 'ul'), None)
            text_b = "\n".join(f'<p style="color:var(--color-text-light);line-height:1.8;margin-bottom:.75rem;">{p}</p>' for p in parasb)
            arrows_b = ""
            if ulb:
                arrows_b = "<div style='display:flex;flex-direction:column;gap:.5rem;margin-top:.75rem;'>" + "".join(
                    f"<div style='display:flex;gap:.75rem;'><span style='color:var(--color-accent);font-weight:700;flex-shrink:0;'>→</span><span style='color:var(--color-text-light);'>{li.get_text(strip=True)}</span></div>"
                    for li in ulb.find_all('li')
                ) + "</div>"
            new_html.append(f'''
<section class="why" style="background:var(--color-white);">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:start;" class="reveal">
      <div><span class="section-label">{h2a.split()[0]}</span><h2 class="section-title" style="margin-bottom:1.5rem;">{h2a}</h2>{text_a}{arrows_a}</div>
      <div><span class="section-label">{h2b.split()[0]}</span><h2 class="section-title" style="margin-bottom:1.5rem;">{h2b}</h2>{text_b}{arrows_b}</div>
    </div>
  </div>
</section>''')
            i += 2
        else:
            new_html.append(f'''
<section class="why" style="background:var(--color-white);">
  <div class="container">
    <div class="reveal" style="max-width:800px;margin:0 auto;">
      <h2 class="section-title" style="margin-bottom:1.5rem;">{h2a}</h2>
      {text_a}{arrows_a}
    </div>
  </div>
</section>''')
            i += 1

    # Services Available (dark grid of link cards)
    svc_section = next((s for s in sections if 'service' in s[0].lower() and 'available' in s[0].lower()), None)
    if not svc_section:
        svc_section = next((s for s in sections if 'service' in s[0].lower()), None)
    if svc_section:
        h2s, _ = svc_section
        new_html.append(f'''
<section class="why">
  <div class="container">
    <div class="why__header reveal">
      <h2 class="section-title">{h2s}</h2>
      <p class="section-subtitle">Full-service HVAC — repair, installation, maintenance, and 24/7 emergencies in {m["city"]}.</p>
    </div>
    {service_link_cards(SVC_LINKS)}
  </div>
</section>''')

    new_section = "\n".join(new_html)
    result = re.sub(
        r'<section class="loc-content">.*?</section>(?=\s*<!--)',
        new_section,
        html,
        flags=re.DOTALL
    )
    if result == html:
        result = re.sub(
            r'<section class="loc-content">.*?</section>',
            new_section,
            html,
            flags=re.DOTALL,
            count=1
        )
    return result


# ─── PAGE METADATA ─────────────────────────────────────────────────────────────
SVC_META = {
    "ac-installation.html": {
        "badge": "AC Installation Huntsville, AL",
        "intro_cards": [
            ("🏠", "Manual J Load Calc", "Exact sizing for your home's square footage and exposure"),
            ("📋", "Written Quote", "Full system cost in writing before any work begins"),
            ("🔧", "All Major Brands", "Carrier, Trane, Lennox, Rheem, Goodman"),
            ("✅", "Tested & Verified", "Temperature, airflow, refrigerant — all checked"),
        ],
        "cta_h": "Ready for a New AC System?",
        "cta_p": "Free in-home assessment, Manual J load calculation, and written quote. No obligation, no pressure.",
    },
    "heating.html": {
        "badge": "Heating Service Huntsville, AL",
        "intro_cards": [
            ("🔥", "All System Types", "Gas furnace, electric furnace, heat pump, dual-fuel"),
            ("⚡", "Same Day", "Most heating calls serviced same day"),
            ("📋", "Written Quote", "Price in writing before any work starts"),
            ("✅", "24/7 Emergency", "No-heat emergencies get priority dispatch"),
        ],
        "cta_h": "Heating System Not Working?",
        "cta_p": "Same-day heating repair in Huntsville. Written quote before work starts. No surprises.",
    },
    "maintenance.html": {
        "badge": "HVAC Maintenance Huntsville, AL",
        "intro_cards": [
            ("📅", "Twice Yearly", "Spring AC tune-up + fall heating tune-up"),
            ("⚡", "Priority Scheduling", "Plan members jump the queue"),
            ("💰", "Repair Discounts", "Members save on any needed repairs"),
            ("✅", "Proactive", "Catch problems before they cause breakdowns"),
        ],
        "cta_h": "Ready to Protect Your HVAC Investment?",
        "cta_p": "A $149/year maintenance plan prevents $1,500+ emergency repair bills. Call now to get started.",
    },
    "emergency.html": {
        "badge": "24/7 Emergency HVAC Huntsville",
        "intro_cards": [
            ("🚨", "24/7 Response", "We dispatch for emergencies day or night"),
            ("⚡", "2–4 Hour Target", "Our response window for emergency calls"),
            ("📋", "Written Quote", "Even on emergency calls — price before work"),
            ("🔧", "Parts on Van", "Common repair parts stocked for fast fixes"),
        ],
        "cta_h": "HVAC Emergency Right Now?",
        "cta_p": "Call immediately. We dispatch 24/7 for genuine emergencies and target 2–4 hours to your door.",
    },
}

LOC_META_DEFAULTS = {
    "intro_cards": [
        ("⚡", "Same Day", "Response for most calls"),
        ("📋", "Written Quote", "Before we touch anything"),
        ("🔧", "All Brands", "Carrier, Trane, Lennox & more"),
        ("⏰", "24/7", "Emergency service available"),
    ],
}

LOC_META = {
    "athens.html":       {"city": "Athens"},
    "decatur.html":      {"city": "Decatur"},
    "guntersville.html": {"city": "Guntersville"},
    "hampton-cove.html": {"city": "Hampton Cove"},
    "hartselle.html":    {"city": "Hartselle"},
    "harvest.html":      {"city": "Harvest"},
    "jones-valley.html": {"city": "Jones Valley"},
    "meridianville.html":{"city": "Meridianville"},
    "scottsboro.html":   {"city": "Scottsboro"},
}
for v in LOC_META.values():
    v.setdefault("intro_cards", LOC_META_DEFAULTS["intro_cards"])


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    changed = []

    # Service pages
    for fname, meta in SVC_META.items():
        path = DOCS / "services" / fname
        if not path.exists():
            print(f"⚠️  Not found: {path}")
            continue
        print(f"Processing: services/{fname}")
        html = path.read_text()
        new_html = rebuild_svc_content(html, meta)
        if new_html != html:
            path.write_text(new_html)
            print(f"  ✅ Rebuilt")
            changed.append(str(path))
        else:
            print(f"  ⚠️  No change — regex may not have matched")

    # Location pages
    for fname, meta in LOC_META.items():
        path = DOCS / "locations" / fname
        if not path.exists():
            print(f"⚠️  Not found: {path}")
            continue
        print(f"Processing: locations/{fname}")
        html = path.read_text()
        new_html = rebuild_loc_content(html, meta)
        if new_html != html:
            path.write_text(new_html)
            print(f"  ✅ Rebuilt")
            changed.append(str(path))
        else:
            print(f"  ⚠️  No change — regex may not have matched")

    print(f"\n🎉 Done — {len(changed)}/{len(SVC_META)+len(LOC_META)} pages rebuilt")

if __name__ == "__main__":
    main()
