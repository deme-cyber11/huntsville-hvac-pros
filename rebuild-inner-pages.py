#!/usr/bin/env python3
"""Rebuild about/contact/faq/blog with correct v2.5 class names."""
import re
from pathlib import Path

DOCS = Path("/Users/costa.demetral/Documents/Rank and Rent $/My-RR-Sites/Huntsville-HVAC-Pros/docs")

NAV = """\
<nav class="nav" id="mainNav">
  <div class="nav__inner">
    <a href="/" class="nav__logo">Huntsville <span>HVAC</span> Pros</a>
    <ul class="nav__links" id="navLinks">
      <li><a href="/services/ac-repair.html">Services</a></li>
      <li><a href="/about.html">About</a></li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/locations/madison.html">Areas</a></li>
      <li><a href="/faq.html">FAQ</a></li>
      <li><a href="/contact.html">Contact</a></li>
      <li><a href="tel:+12562159287" class="nav__cta">Call Now</a></li>
    </ul>
    <button class="nav__toggle" id="navToggle" aria-label="Open menu">
      <svg viewBox="0 0 24 24"><path d="M3 12h18M3 6h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg>
    </button>
  </div>
</nav>"""

FOOTER = """\
<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div class="footer__col footer__col--brand">
        <div class="footer__brand-name">Huntsville <span>HVAC</span> Pros</div>
        <p class="footer__brand-desc">Licensed and insured HVAC contractors serving Huntsville, Alabama and surrounding areas. Honest diagnostics, written quotes, no pressure sales. Serving North Alabama since 2009.</p>
        <div class="footer__contact-item"><a href="tel:+12562159287">(256) 215-9287</a></div>
        <div class="footer__contact-item"><a href="mailto:info@huntsvillehvacpros.com">info@huntsvillehvacpros.com</a></div>
      </div>
      <div class="footer__col">
        <h4 class="footer__heading">Services</h4>
        <ul class="footer__links">
          <li><a href="/services/ac-repair.html">AC Repair</a></li>
          <li><a href="/services/ac-installation.html">AC Installation</a></li>
          <li><a href="/services/heating.html">Heating</a></li>
          <li><a href="/services/maintenance.html">Maintenance</a></li>
          <li><a href="/services/emergency.html">Emergency</a></li>
        </ul>
      </div>
      <div class="footer__col">
        <h4 class="footer__heading">Company</h4>
        <ul class="footer__links">
          <li><a href="/about.html">About</a></li>
          <li><a href="/locations/madison.html">Service Areas</a></li>
          <li><a href="/blog/">Blog</a></li>
          <li><a href="/faq.html">FAQ</a></li>
          <li><a href="/contact.html">Contact</a></li>
        </ul>
      </div>
      <div class="footer__col">
        <h4 class="footer__heading">Contact</h4>
        <div class="footer__contact-item"><a href="tel:+12562159287">(256) 215-9287</a></div>
        <div class="footer__contact-item">info@huntsvillehvacpros.com</div>
        <div class="footer__contact-item">Serving Huntsville, Madison &amp; all of Madison County, AL</div>
      </div>
    </div>
    <div class="footer__bottom">
      <span class="footer__copy">&copy; 2026 Huntsville HVAC Pros. All rights reserved.</span>
      <div class="footer__legal">
        <a href="/privacy.html">Privacy Policy</a>
        <a href="/sitemap.xml">Sitemap</a>
      </div>
    </div>
  </div>
</footer>"""

MOBILE_CTA = """\
<div class="mobile-cta">
  <a href="tel:+12562159287" class="mobile-cta__btn mobile-cta__btn--call">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 01.01 1.18 2 2 0 012 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>
    Call Now
  </a>
  <a href="/contact.html" class="mobile-cta__btn mobile-cta__btn--estimate">Free Estimate</a>
</div>"""

JS_BLOCK = """\
<script>
document.documentElement.classList.add("js");
const nav = document.getElementById('mainNav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 60);
}, { passive: true });
document.getElementById('navToggle').addEventListener('click', () => {
  document.getElementById('navLinks').classList.toggle('open');
});
document.querySelectorAll('.faq__question').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq__item');
    const isOpen = item.classList.contains('active');
    document.querySelectorAll('.faq__item').forEach(i => i.classList.remove('active'));
    if (!isOpen) item.classList.add('active');
  });
});
const revealEls = document.querySelectorAll('.reveal');
if (revealEls.length) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); }
    });
  }, { threshold: 0.15 });
  revealEls.forEach(el => observer.observe(el));
}
</script>"""

def head_from(path):
    """Extract <head> block from existing page, ensuring correct CSS path."""
    html = path.read_text()
    head = re.search(r'<head>.*?</head>', html, re.DOTALL).group(0)
    # Ensure correct CSS path
    head = re.sub(r'href=["\']css/style\.v2\.5\.css["\']', 'href="/css/style.v2.5.css"', head)
    return head

def build_page(head, body_html):
    return f"""<!DOCTYPE html>
<html lang="en">
{head}
<body>
{NAV}
{body_html}
{FOOTER}
{MOBILE_CTA}
{JS_BLOCK}
</body>
</html>"""


# ══════════════════════════════════════════════════
# ABOUT
# ══════════════════════════════════════════════════
about_body = """\
<section class="hero hero--inner">
  <div class="hero__bg" style="background-image:url('/images/hero-main.webp');"></div>
  <div class="hero__orb hero__orb--1"></div>
  <div class="hero__orb hero__orb--2"></div>
  <div class="container">
    <div class="hero__content" style="max-width:720px;">
      <span class="hero__badge">15+ Years Serving Huntsville, AL</span>
      <h1 class="hero__title">About Huntsville HVAC Pros</h1>
      <p class="hero__subtitle">Licensed, insured, and honest. We built this company because Huntsville deserved an HVAC contractor that actually tells you the truth.</p>
    </div>
  </div>
</section>

<section class="trust-bar">
  <div class="container">
    <div class="trust-bar__inner">
      <div class="trust-bar__item"><div class="trust-bar__icon">🏆</div><div><strong>15+</strong><span>Years Experience</span></div></div>
      <div class="trust-bar__item"><div class="trust-bar__icon">🔧</div><div><strong>3,800+</strong><span>Systems Serviced</span></div></div>
      <div class="trust-bar__item"><div class="trust-bar__icon">⚡</div><div><strong>24/7</strong><span>Emergency Service</span></div></div>
      <div class="trust-bar__item"><div class="trust-bar__icon">✅</div><div><strong>100%</strong><span>Satisfaction Guarantee</span></div></div>
    </div>
  </div>
</section>

<section class="why" style="background:var(--color-white);">
  <div class="container">
    <div class="why__inner">
      <div class="why__content reveal">
        <h2 class="section-title">Our Story</h2>
        <p class="why__text">Huntsville HVAC Pros was founded with a simple idea: HVAC service should be honest, transparent, and fair. Too many homeowners in the Huntsville area have experienced the frustration of paying for repairs they did not need, or being told their entire system needed replacement when the real problem was a $200 part.</p>
        <p class="why__text">We started this company because we believed Huntsville deserved an HVAC contractor that diagnoses honestly, quotes in writing before touching anything, and charges what was quoted. That commitment has not changed in over 15 years of service across Madison County.</p>
        <h3 style="margin-top:2rem;margin-bottom:1rem;color:var(--color-dark);">Our Mission</h3>
        <p class="why__text">Every job gets a written diagnosis and price before any work starts. If we find something unexpected mid-repair, we stop and show you before proceeding. We give you both the repair cost and the replacement cost when it is a borderline decision, and we let you choose without pressure. We show you the broken part. We explain why it failed. We treat your home and your time with respect.</p>
        <h3 style="margin-top:2rem;margin-bottom:1rem;color:var(--color-dark);">Our Team Values</h3>
        <p class="why__text">Every technician on our team is licensed by the Alabama Licensing Board for General Contractors, EPA certified for refrigerant handling, and background checked. We hire people who can explain what is wrong with your system in plain language, not jargon. Our team communicates clearly because we believe informed homeowners make better decisions.</p>
      </div>
      <div class="why__image reveal">
        <img src="/images/about-team.webp" alt="Huntsville HVAC Pros licensed technician team" width="540" height="480" loading="lazy">
      </div>
    </div>
  </div>
</section>

<section class="why">
  <div class="container">
    <div class="why__header reveal">
      <h2 class="section-title">Why Choose Huntsville HVAC Pros</h2>
      <p class="section-subtitle">What sets us apart from other HVAC contractors in the Huntsville area.</p>
    </div>
    <div class="why__stats" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.5rem;margin-top:3rem;">
      <div class="why__stat-card reveal"><h3>Licensed &amp; Insured</h3><p>Full HVAC contractor licensing through the Alabama Licensing Board. Comprehensive liability and workers' compensation insurance on every job.</p></div>
      <div class="why__stat-card reveal"><h3>Same-Day Response</h3><p>We dispatch technicians the same day for most calls and 24/7 for emergencies. No waiting three days in an Alabama heat wave.</p></div>
      <div class="why__stat-card reveal"><h3>Upfront Pricing</h3><p>We quote before we start. What we say it costs is what you pay. No verbal estimates, no surprises, no "while we were in there" add-ons.</p></div>
      <div class="why__stat-card reveal"><h3>Local Team</h3><p>When you call (256) 215-9287, a Huntsville team member answers. Not a national dispatch center. We know your neighborhood because we live here.</p></div>
      <div class="why__stat-card reveal"><h3>EPA Certified</h3><p>All technicians hold EPA Section 608 certification for refrigerant handling. We follow all environmental and safety regulations.</p></div>
      <div class="why__stat-card reveal"><h3>Honest Recommendations</h3><p>We give you both the repair cost and replacement cost when it is a close call. We explain the pros and cons and let you decide.</p></div>
    </div>
  </div>
</section>

<section class="cta">
  <div class="container">
    <div class="cta__inner reveal">
      <span class="cta__urgency">Free Estimates · No Pressure · Same-Day Service Available</span>
      <h2 class="cta__title">Ready to Work with an HVAC Team You Can Trust?</h2>
      <p class="cta__desc">Call now for same-day service or request a free estimate. No obligation.</p>
      <div class="cta__buttons">
        <a href="tel:+12562159287" class="btn btn--primary">Call (256) 215-9287</a>
        <a href="/contact.html" class="btn btn--outline">Get Free Estimate</a>
      </div>
    </div>
  </div>
</section>"""

# ══════════════════════════════════════════════════
# CONTACT
# ══════════════════════════════════════════════════
contact_body = """\
<section class="hero hero--inner">
  <div class="hero__bg" style="background-image:url('/images/hero-main.webp');"></div>
  <div class="hero__orb hero__orb--1"></div>
  <div class="hero__orb hero__orb--2"></div>
  <div class="container">
    <div class="hero__content" style="max-width:720px;">
      <span class="hero__badge">Same-Day Service Available</span>
      <h1 class="hero__title">Contact Huntsville HVAC Pros</h1>
      <p class="hero__subtitle">Call, text, or submit a request. We respond fast — most calls are answered same day.</p>
      <div class="hero__buttons">
        <a href="tel:+12562159287" class="btn btn--primary">Call (256) 215-9287</a>
      </div>
    </div>
  </div>
</section>

<section class="trust-bar">
  <div class="container">
    <div class="trust-bar__inner">
      <div class="trust-bar__item"><div class="trust-bar__icon">⚡</div><div><strong>Same Day</strong><span>Response</span></div></div>
      <div class="trust-bar__item"><div class="trust-bar__icon">🕐</div><div><strong>24/7</strong><span>Emergency Service</span></div></div>
      <div class="trust-bar__item"><div class="trust-bar__icon">📋</div><div><strong>Free</strong><span>Estimates</span></div></div>
      <div class="trust-bar__item"><div class="trust-bar__icon">✅</div><div><strong>No</strong><span>Pressure</span></div></div>
    </div>
  </div>
</section>

<section class="why" style="background:var(--color-white);">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:start;" class="reveal">
      <div>
        <h2 class="section-title" style="margin-bottom:2rem;">Get in Touch</h2>
        <div style="display:flex;flex-direction:column;gap:1.5rem;margin-bottom:2.5rem;">
          <div style="display:flex;gap:1rem;align-items:flex-start;">
            <div style="width:48px;height:48px;border-radius:12px;background:rgba(14,165,233,0.1);display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0;">📞</div>
            <div><strong style="display:block;color:var(--color-dark);margin-bottom:.25rem;">Phone</strong><a href="tel:+12562159287" style="color:var(--color-accent);font-size:1.125rem;font-weight:700;">(256) 215-9287</a><br><small style="color:var(--color-text-light);">Mon–Fri 7am–7pm · Sat 8am–5pm · 24/7 for emergencies</small></div>
          </div>
          <div style="display:flex;gap:1rem;align-items:flex-start;">
            <div style="width:48px;height:48px;border-radius:12px;background:rgba(14,165,233,0.1);display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0;">✉️</div>
            <div><strong style="display:block;color:var(--color-dark);margin-bottom:.25rem;">Email</strong><a href="mailto:info@huntsvillehvacpros.com" style="color:var(--color-accent);">info@huntsvillehvacpros.com</a></div>
          </div>
          <div style="display:flex;gap:1rem;align-items:flex-start;">
            <div style="width:48px;height:48px;border-radius:12px;background:rgba(14,165,233,0.1);display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0;">📍</div>
            <div><strong style="display:block;color:var(--color-dark);margin-bottom:.25rem;">Service Area</strong><span style="color:var(--color-text-light);">Huntsville, Madison, Hampton Cove, Jones Valley, Meridianville, Harvest, Decatur &amp; all of Madison County, AL</span></div>
          </div>
        </div>
      </div>
      <div>
        <h2 class="section-title" style="margin-bottom:2rem;">Request a Free Estimate</h2>
        <form action="https://api.web3forms.com/submit" method="POST" style="display:flex;flex-direction:column;gap:1rem;">
          <input type="hidden" name="access_key" value="0219881f-13e5-4175-b720-517b8d10c028">
          <input type="hidden" name="subject" value="New HVAC Estimate Request — HuntsvilleHVACPros.com">
          <input type="hidden" name="redirect" value="https://huntsvillehvacpros.com/thank-you.html">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
            <div><label style="display:block;font-size:.875rem;font-weight:600;margin-bottom:.5rem;color:var(--color-dark);">Your Name *</label><input type="text" name="name" required placeholder="John Smith" style="width:100%;padding:.75rem 1rem;border:1px solid #e2e8f0;border-radius:8px;font-size:1rem;outline:none;"></div>
            <div><label style="display:block;font-size:.875rem;font-weight:600;margin-bottom:.5rem;color:var(--color-dark);">Phone *</label><input type="tel" name="phone" required placeholder="(256) 555-0100" style="width:100%;padding:.75rem 1rem;border:1px solid #e2e8f0;border-radius:8px;font-size:1rem;outline:none;"></div>
          </div>
          <div><label style="display:block;font-size:.875rem;font-weight:600;margin-bottom:.5rem;color:var(--color-dark);">Email</label><input type="email" name="email" placeholder="you@example.com" style="width:100%;padding:.75rem 1rem;border:1px solid #e2e8f0;border-radius:8px;font-size:1rem;outline:none;"></div>
          <div><label style="display:block;font-size:.875rem;font-weight:600;margin-bottom:.5rem;color:var(--color-dark);">Service Needed</label><select name="service" style="width:100%;padding:.75rem 1rem;border:1px solid #e2e8f0;border-radius:8px;font-size:1rem;outline:none;background:white;"><option value="">Select a service...</option><option>AC Repair</option><option>AC Installation / Replacement</option><option>Heating Repair</option><option>Furnace Replacement</option><option>Preventive Maintenance</option><option>24/7 Emergency</option><option>Other</option></select></div>
          <div><label style="display:block;font-size:.875rem;font-weight:600;margin-bottom:.5rem;color:var(--color-dark);">Message</label><textarea name="message" rows="4" placeholder="Describe your HVAC issue or what you need..." style="width:100%;padding:.75rem 1rem;border:1px solid #e2e8f0;border-radius:8px;font-size:1rem;outline:none;resize:vertical;"></textarea></div>
          <button type="submit" class="btn btn--primary" style="width:100%;justify-content:center;">Send Request →</button>
          <p style="font-size:.8125rem;color:var(--color-text-light);text-align:center;">We respond within 2 hours during business hours.</p>
        </form>
      </div>
    </div>
  </div>
</section>

<section class="cta">
  <div class="container">
    <div class="cta__inner reveal">
      <span class="cta__urgency">24/7 Emergency Line Available</span>
      <h2 class="cta__title">AC Not Cooling? Don't Wait.</h2>
      <p class="cta__desc">In an Alabama summer, a broken AC is an emergency. Call us now — we dispatch same day.</p>
      <div class="cta__buttons">
        <a href="tel:+12562159287" class="btn btn--primary">Call (256) 215-9287</a>
      </div>
    </div>
  </div>
</section>"""

# ══════════════════════════════════════════════════
# FAQ
# ══════════════════════════════════════════════════
faq_body = """\
<section class="hero hero--inner">
  <div class="hero__bg" style="background-image:url('/images/hero-main.webp');"></div>
  <div class="hero__orb hero__orb--1"></div>
  <div class="hero__orb hero__orb--2"></div>
  <div class="container">
    <div class="hero__content" style="max-width:720px;">
      <span class="hero__badge">Huntsville HVAC Questions Answered</span>
      <h1 class="hero__title">Frequently Asked Questions</h1>
      <p class="hero__subtitle">Honest answers to the questions Huntsville homeowners ask most about HVAC repair, replacement, and maintenance.</p>
    </div>
  </div>
</section>

<section class="faq" style="background:var(--color-white);padding:5rem 0;">
  <div class="container">
    <div class="faq__header reveal">
      <h2 class="section-title">HVAC Questions &amp; Answers</h2>
      <p class="section-subtitle">Can't find your answer? Call us at <a href="tel:+12562159287" style="color:var(--color-accent);">(256) 215-9287</a> — we're happy to help.</p>
    </div>
    <div class="faq__list reveal">
      <div class="faq__item">
        <button class="faq__question">How quickly can you get to my home?<span class="faq__icon">+</span></button>
        <div class="faq__answer"><p>For most service calls, we can dispatch a technician the same day. For 24/7 emergencies — a completely failed AC in summer or a no-heat situation in winter — we respond immediately regardless of the hour. Call <a href="tel:+12562159287">(256) 215-9287</a>.</p></div>
      </div>
      <div class="faq__item">
        <button class="faq__question">Do you charge for diagnostics?<span class="faq__icon">+</span></button>
        <div class="faq__answer"><p>We charge a diagnostic fee to come out and identify the problem. That fee is credited toward your repair if you proceed with us. You will always know what the diagnosis fee is before we show up — no surprises.</p></div>
      </div>
      <div class="faq__item">
        <button class="faq__question">Should I repair or replace my AC?<span class="faq__icon">+</span></button>
        <div class="faq__answer"><p>We give you both options and the honest math. General rule: if your system is under 10 years old and the repair is under $800, repair usually makes sense. Over 15 years old or repair cost exceeds 50% of a new system — replacement is typically smarter. We never push replacement to sell you something you don't need.</p></div>
      </div>
      <div class="faq__item">
        <button class="faq__question">How much does HVAC repair cost in Huntsville?<span class="faq__icon">+</span></button>
        <div class="faq__answer"><p>Costs vary by the issue. Refrigerant recharge: $150–$400. Capacitor or contactor replacement: $150–$300. Blower motor: $300–$600. Compressor replacement: $1,200–$2,500. Full system replacement: $4,500–$12,000 depending on size and efficiency. We provide written quotes before any work starts.</p></div>
      </div>
      <div class="faq__item">
        <button class="faq__question">What brands do you service?<span class="faq__icon">+</span></button>
        <div class="faq__answer"><p>We service all major brands including Carrier, Trane, Lennox, Rheem, Goodman, York, American Standard, and others. Our technicians are trained on equipment from all major manufacturers.</p></div>
      </div>
      <div class="faq__item">
        <button class="faq__question">Do you offer maintenance plans?<span class="faq__icon">+</span></button>
        <div class="faq__answer"><p>Yes. Our maintenance plan includes two tune-ups per year (spring AC and fall heating), priority scheduling, and discounts on repairs. Regular maintenance extends equipment life and catches small problems before they become expensive failures.</p></div>
      </div>
      <div class="faq__item">
        <button class="faq__question">Are your technicians licensed and insured?<span class="faq__icon">+</span></button>
        <div class="faq__answer"><p>Yes. All technicians are licensed through the Alabama Licensing Board for General Contractors, EPA Section 608 certified for refrigerant handling, and background checked. We carry full liability and workers' compensation insurance on every job.</p></div>
      </div>
      <div class="faq__item">
        <button class="faq__question">What areas do you serve?<span class="faq__icon">+</span></button>
        <div class="faq__answer"><p>We serve Huntsville and all of Madison County, including Madison, Hampton Cove, Jones Valley, Meridianville, Harvest, Decatur, Athens, Guntersville, and surrounding areas. Not sure if we cover your location? Call us.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="cta">
  <div class="container">
    <div class="cta__inner reveal">
      <span class="cta__urgency">Same-Day Service Available · Free Estimates</span>
      <h2 class="cta__title">Still Have Questions? Call Us.</h2>
      <p class="cta__desc">We're happy to answer anything over the phone — no obligation, no sales pitch.</p>
      <div class="cta__buttons">
        <a href="tel:+12562159287" class="btn btn--primary">Call (256) 215-9287</a>
        <a href="/contact.html" class="btn btn--outline">Get Free Estimate</a>
      </div>
    </div>
  </div>
</section>"""

# ══════════════════════════════════════════════════
# BLOG INDEX
# ══════════════════════════════════════════════════
blog_body = """\
<section class="hero hero--inner">
  <div class="hero__bg" style="background-image:url('/images/hero-main.webp');"></div>
  <div class="hero__orb hero__orb--1"></div>
  <div class="hero__orb hero__orb--2"></div>
  <div class="container">
    <div class="hero__content" style="max-width:720px;">
      <span class="hero__badge">HVAC Tips for Huntsville Homeowners</span>
      <h1 class="hero__title">HVAC Resources &amp; Guides</h1>
      <p class="hero__subtitle">Practical advice on AC repair, heating, maintenance, and everything HVAC in North Alabama.</p>
    </div>
  </div>
</section>

<section class="why" style="background:var(--color-white);padding:5rem 0;">
  <div class="container">
    <div class="why__header reveal">
      <h2 class="section-title">Latest Articles</h2>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:2rem;margin-top:3rem;">
      <a href="/blog/signs-ac-needs-repair.html" class="bento__card reveal" style="text-decoration:none;">
        <div style="height:200px;background:linear-gradient(135deg,var(--color-dark) 0%,var(--color-accent) 100%);border-radius:12px 12px 0 0;display:flex;align-items:center;justify-content:center;font-size:3rem;">❄️</div>
        <div style="padding:1.5rem;">
          <span style="font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--color-accent);">AC Repair</span>
          <h3 style="margin:.5rem 0 .75rem;color:var(--color-dark);">5 Signs Your AC Needs Repair Before Summer</h3>
          <p style="color:var(--color-text-light);font-size:.9375rem;line-height:1.6;">Catch small problems before they become expensive failures. These warning signs mean it's time to call.</p>
          <span class="bento__link" style="opacity:1;transform:none;margin-top:1rem;display:inline-flex;align-items:center;gap:.5rem;color:var(--color-accent);font-weight:700;font-size:.875rem;">Read Article →</span>
        </div>
      </a>
      <a href="/blog/summer-ac-prep-huntsville.html" class="bento__card reveal" style="text-decoration:none;">
        <div style="height:200px;background:linear-gradient(135deg,#1e3a5f 0%,#f97316 100%);border-radius:12px 12px 0 0;display:flex;align-items:center;justify-content:center;font-size:3rem;">☀️</div>
        <div style="padding:1.5rem;">
          <span style="font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--color-accent);">Maintenance</span>
          <h3 style="margin:.5rem 0 .75rem;color:var(--color-dark);">How to Prep Your HVAC for Huntsville Summers</h3>
          <p style="color:var(--color-text-light);font-size:.9375rem;line-height:1.6;">Huntsville summers are brutal. Here's how to make sure your system is ready before the heat hits.</p>
          <span class="bento__link" style="opacity:1;transform:none;margin-top:1rem;display:inline-flex;align-items:center;gap:.5rem;color:var(--color-accent);font-weight:700;font-size:.875rem;">Read Article →</span>
        </div>
      </a>
      <a href="/blog/choosing-hvac-system-huntsville.html" class="bento__card reveal" style="text-decoration:none;">
        <div style="height:200px;background:linear-gradient(135deg,#1a2744 0%,#22c55e 100%);border-radius:12px 12px 0 0;display:flex;align-items:center;justify-content:center;font-size:3rem;">🏠</div>
        <div style="padding:1.5rem;">
          <span style="font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--color-accent);">Buying Guide</span>
          <h3 style="margin:.5rem 0 .75rem;color:var(--color-dark);">Choosing the Right HVAC System for Your Huntsville Home</h3>
          <p style="color:var(--color-text-light);font-size:.9375rem;line-height:1.6;">SEER ratings, tonnage, heat pumps vs. gas furnaces — what actually matters for North Alabama homes.</p>
          <span class="bento__link" style="opacity:1;transform:none;margin-top:1rem;display:inline-flex;align-items:center;gap:.5rem;color:var(--color-accent);font-weight:700;font-size:.875rem;">Read Article →</span>
        </div>
      </a>
      <a href="/blog/how-much-does-hvac-cost-huntsville.html" class="bento__card reveal" style="text-decoration:none;">
        <div style="height:200px;background:linear-gradient(135deg,#1e293b 0%,#8b5cf6 100%);border-radius:12px 12px 0 0;display:flex;align-items:center;justify-content:center;font-size:3rem;">💰</div>
        <div style="padding:1.5rem;">
          <span style="font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--color-accent);">Pricing</span>
          <h3 style="margin:.5rem 0 .75rem;color:var(--color-dark);">How Much Does HVAC Repair Cost in Huntsville?</h3>
          <p style="color:var(--color-text-light);font-size:.9375rem;line-height:1.6;">Real price ranges for common repairs and replacements. Know what to expect before you call.</p>
          <span class="bento__link" style="opacity:1;transform:none;margin-top:1rem;display:inline-flex;align-items:center;gap:.5rem;color:var(--color-accent);font-weight:700;font-size:.875rem;">Read Article →</span>
        </div>
      </a>
    </div>
  </div>
</section>

<section class="cta">
  <div class="container">
    <div class="cta__inner reveal">
      <span class="cta__urgency">Same-Day Service · Free Estimates</span>
      <h2 class="cta__title">Ready to Fix Your HVAC?</h2>
      <p class="cta__desc">Don't wait until it breaks down completely. Call Huntsville's most trusted HVAC team.</p>
      <div class="cta__buttons">
        <a href="tel:+12562159287" class="btn btn--primary">Call (256) 215-9287</a>
        <a href="/contact.html" class="btn btn--outline">Get Free Estimate</a>
      </div>
    </div>
  </div>
</section>"""


# ══════════════════════════════════════════════════
# WRITE PAGES
# ══════════════════════════════════════════════════
pages = [
    (DOCS / "about.html", about_body),
    (DOCS / "contact.html", contact_body),
    (DOCS / "faq.html", faq_body),
    (DOCS / "blog/index.html", blog_body),
]

for path, body in pages:
    head = head_from(path)
    html = build_page(head, body)
    path.write_text(html)
    print(f"✅ Rebuilt: {path.name}")


# ══════════════════════════════════════════════════
# FIX BLOG POSTS — nav + footer + JS only
# ══════════════════════════════════════════════════
blog_posts = list((DOCS / "blog").glob("*.html"))
blog_posts = [p for p in blog_posts if p.name != "index.html"]

for path in blog_posts:
    html = path.read_text()

    # Fix CSS path
    html = re.sub(r'href=["\']css/style\.v2\.5\.css["\']', 'href="/css/style.v2.5.css"', html)
    html = re.sub(r'href=["\']\.\.\/css/style\.v2\.5\.css["\']', 'href="/css/style.v2.5.css"', html)
    html = re.sub(r'href=["\']style\.v2\.5\.css["\']', 'href="/css/style.v2.5.css"', html)

    # Replace broken nav block
    html = re.sub(
        r'<!--\s*={0,5}\s*NAV\s*={0,5}\s*-->.*?</header>',
        f'<!-- NAV -->\n{NAV}',
        html, flags=re.DOTALL
    )
    # Also try without comment
    html = re.sub(
        r'<header class="site-header"[^>]*>.*?</header>',
        NAV,
        html, flags=re.DOTALL
    )

    # Replace broken footer
    html = re.sub(
        r'<footer class="site-footer".*?</footer>',
        FOOTER,
        html, flags=re.DOTALL
    )

    # Replace broken mobile CTA
    html = re.sub(
        r'<div class="mobile-cta">.*?</div>\s*\n\s*\n',
        MOBILE_CTA + '\n\n',
        html, flags=re.DOTALL
    )

    # Replace broken script block
    html = re.sub(
        r'<script>\s*const header.*?</script>',
        JS_BLOCK,
        html, flags=re.DOTALL
    )

    path.write_text(html)
    print(f"✅ Fixed nav/footer: {path.name}")


# Fix privacy + thank-you
for name in ["privacy.html", "thank-you.html"]:
    path = DOCS / name
    if not path.exists():
        continue
    html = path.read_text()
    html = re.sub(r'href=["\']css/style\.v2\.5\.css["\']', 'href="/css/style.v2.5.css"', html)
    html = re.sub(
        r'<!--\s*={0,5}\s*NAV\s*={0,5}\s*-->.*?</header>',
        f'<!-- NAV -->\n{NAV}',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'<header class="site-header"[^>]*>.*?</header>',
        NAV,
        html, flags=re.DOTALL
    )
    html = re.sub(r'<footer class="site-footer".*?</footer>', FOOTER, html, flags=re.DOTALL)
    html = re.sub(r'<script>\s*const header.*?</script>', JS_BLOCK, html, flags=re.DOTALL)
    path.write_text(html)
    print(f"✅ Fixed nav/footer: {name}")

print("\n🎉 All done!")
