#!/usr/bin/env python3
"""Build The Strip static site from shared chrome + page content."""
import os
from pathlib import Path

STAGING = os.environ.get("STAGING") == "1"

ROOT = Path(__file__).parent
SITE = "https://www.thestripphotobooth.co.za"
EMAIL = "hello@thestripphotobooth.co.za"
YEAR = "2026"

IMAGES = [
    ("gallery-01.jpg", "Black-and-white booth portrait"),
    ("gallery-02.jpg", "A couple sharing a kiss in the booth"),
    ("gallery-03.jpg", "Four friends posing together"),
    ("gallery-04.jpg", "A guest posing in sunglasses"),
    ("gallery-05.jpg", "A couple posing cheek to cheek"),
    ("gallery-06.jpg", "A couple in front of the booth curtain"),
    ("gallery-07.jpg", "Four friends smiling for the camera"),
    ("gallery-08.jpg", "A couple making playful faces"),
    ("gallery-09.jpg", "Friends posing for a group photo"),
    ("gallery-10.jpg", "A couple sharing a moment"),
    ("gallery-11.jpg", "Five friends in a black-and-white booth photo"),
    ("gallery-12.jpg", "Three friends smiling in the booth"),
]

PRINT_IMAGES = [(f"gallery-print-{i:02d}.jpg", alt) for i, (_, alt) in enumerate(IMAGES, 1)]

NAV = [
    ("about.html", "Experience", "about"),
    ("gallery.html", "Gallery", "gallery"),
    ("packages.html", "Packages", "packages"),
    ("how-it-works.html", "How it works", "how-it-works"),
    ("faq.html", "FAQ", "faq"),
    ("contact.html", "Enquire", "contact"),
]

def esc(value: str) -> str:
    return (value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))

def layout(slug, title, description, content, active=None, head_extra="", noindex=False):
    canonical = SITE + ("/" if slug == "index" else f"/{slug}.html")
    nav_html = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if active == key else ""}>{esc(label)}{" ↗" if key == "contact" else ""}</a>'
        for href, label, key in NAV
    )
    robots = '<meta name="robots" content="noindex,nofollow">' if noindex or STAGING else '<meta name="robots" content="index,follow">'
    return f"""<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#F4F3EF">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The Strip">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{SITE}/assets/og-image.jpg">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="css/site.css">
{head_extra}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header>
  <a class="wordmark" href="index.html" aria-label="The Strip home">The Strip</a>
  <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav id="nav" aria-label="Main navigation">{nav_html}</nav>
</header>
<main id="main">
{content}
</main>
<footer>
  <a class="wordmark" href="index.html">The Strip</a>
  <nav aria-label="Footer navigation">
    <a href="about.html">Experience</a>
    <a href="gallery.html">Gallery</a>
    <a href="packages.html">Packages</a>
    <a href="how-it-works.html">How it works</a>
    <a href="faq.html">FAQ</a>
  </nav>
  <div class="legal">
    <a href="privacy.html">Privacy</a>
    <a href="terms.html">Terms</a>
    <a href="contact.html">Enquire ↗</a>
  </div>
  <span>© <span data-year>{YEAR}</span> The Strip. All rights reserved.</span>
</footer>
<script src="js/config.js"></script>
<script src="js/site.js" defer></script>
</body>
</html>
"""

def gallery_marquee():
    return "".join(
        f'<div class="portrait"><img src="assets/{name}" alt="{esc(alt)}" loading="{"eager" if i < 3 else "lazy"}" decoding="async"></div>'
        for i, (name, alt) in enumerate(IMAGES)
    )

def gallery_grid():
    return "".join(
        f'<figure><a href="assets/{name}" data-lightbox data-alt="{esc(alt)}" aria-label="Open photo: {esc(alt)}">'
        f'<img src="assets/{name}" alt="{esc(alt)}" loading="lazy" decoding="async"></a>'
        f'<figcaption>No. {i + 1:02d}</figcaption></figure>'
        for i, (name, alt) in enumerate(PRINT_IMAGES)
    )

def lightbox():
    return """<dialog id="lightbox" class="lightbox" aria-label="Photo viewer">
  <div class="lightbox-inner">
    <img alt="">
    <div class="lightbox-bar">
      <span class="caption"></span>
      <div class="lightbox-controls">
        <button type="button" data-prev aria-label="Previous photo">←</button>
        <button type="button" data-next aria-label="Next photo">→</button>
        <button type="button" data-close aria-label="Close photo viewer">✕</button>
      </div>
    </div>
  </div>
</dialog>"""

def page_hero(eyebrow, heading, lede):
    return f'<section class="page-hero"><div class="eyebrow">{esc(eyebrow)}</div><h1>{heading}</h1><p class="lede">{lede}</p></section>'

def cta(heading="See you<br>in The Strip."):
    return f"""<section class="cta">
  <a class="cta-link" href="contact.html">{heading} <span>↗</span></a>
  <a class="email" href="mailto:{EMAIL}">{EMAIL}</a>
</section>"""

def carousel_tools():
    return """<div class="gallery-tools">
    <span>A LITTLE PRIVACY. A LOT OF PERSONALITY.</span>
    <div>
      <button type="button" id="pause-gallery" aria-label="Pause photo animation" aria-pressed="false" aria-controls="track">Ⅱ</button>
      <button type="button" id="prev" aria-label="Previous photograph">←</button>
      <span id="count">01 — 12</span>
      <button type="button" id="next" aria-label="Next photograph">→</button>
    </div>
  </div>"""

# ---------- Home ----------
home = f"""
<section class="gallery" aria-label="Photobooth gallery">
  <div class="gallery-track" id="track">{gallery_marquee()}</div>
  {carousel_tools()}
</section>
<section class="intro">
  <div>
    <h1>Behind the curtain.<br>In the moment.</h1>
    <p class="intro-note">An enclosed photobooth.<br>For your wonderfully unfiltered side.</p>
  </div>
  <a class="round-link" href="#info" aria-label="Discover The Strip">↓</a>
</section>
<section class="info" id="info">
  <div class="eyebrow">01 / MEET THE STRIP</div>
  <div class="info-body">
    <h2>Step in.<br>Let yourself out.</h2>
    <div class="info-copy">
      <p>There’s something about closing the curtain. The outside world fades. The serious faces disappear. And suddenly, it’s just you, your favourite people, and a moment that’s yours.</p>
      <p>The Strip is an enclosed photobooth made for exactly that. A little space to be yourself, and a reason to get everyone in the picture.</p>
      <a class="text-link" href="about.html">More about The Strip <span>↗</span></a>
    </div>
  </div>
</section>
<section class="steps">
  <div class="eyebrow">02 / HOW IT WORKS</div>
  <div class="steps-grid">
    <div class="step"><div class="num">01</div><h3>Enquire.</h3><p>Tell us the date, the place and the kind of night you’re planning.</p></div>
    <div class="step"><div class="num">02</div><h3>We tailor.</h3><p>We shape the booth, the prints and the details around your event.</p></div>
    <div class="step"><div class="num">03</div><h3>Step in.</h3><p>We arrive, set up, and hand the evening over to you and your people.</p></div>
  </div>
  <p class="mt-40"><a class="text-link" href="how-it-works.html">The full story <span>↗</span></a></p>
</section>
<section class="moments">
  <div class="eyebrow">03 / GOOD COMPANY, GREAT MEMORIES</div>
  <div class="occasion"><h3><a href="weddings.html">The big day.<span class="arrow">↗</span></a></h3><p>From your favourite plus-one to the whole wedding party. Make room for the moments between the formal photos.</p><span>01</span></div>
  <div class="occasion"><h3><a href="parties.html">The late night.<span class="arrow">↗</span></a></h3><p>Birthdays, celebrations, and any excuse to get everyone together. Step behind the curtain and see what happens.</p><span>02</span></div>
  <div class="occasion"><h3><a href="corporate.html">The something else.<span class="arrow">↗</span></a></h3><p>A launch, a gathering, a brilliant idea. Tell us what you’re planning and let’s talk about The Strip.</p><span>03</span></div>
</section>
<section class="packages-teaser">
  <div class="eyebrow">04 / PACKAGES</div>
  <h2 style="margin:22px 0 10px">Made for your<br>kind of night.</h2>
  <p class="lede">Every event is different. These are starting points, not boxes — we’ll shape the details around you.</p>
  <div class="package-grid">
    <article class="package-card"><div class="package-tag">01</div><div class="package-name">The Classic</div><div class="package-price">Tailored quote</div><ul class="package-list"><li>Booth, delivery and setup</li><li>Unlimited sessions</li><li>Prints to take home</li><li>Digital gallery</li></ul><a class="package-link" href="packages.html">Explore packages ↗</a></article>
    <article class="package-card"><div class="package-tag">02</div><div class="package-name">The Late Night</div><div class="package-price">Tailored quote</div><ul class="package-list"><li>Everything in The Classic</li><li>Extra hours for the after-party</li><li>Custom print design</li><li>Digital gallery</li></ul><a class="package-link" href="packages.html">Explore packages ↗</a></article>
    <article class="package-card"><div class="package-tag">03</div><div class="package-name">The Something Else</div><div class="package-price">Tailored quote</div><ul class="package-list"><li>For launches and brands</li><li>Branded prints and backdrop</li><li>Attendant on the night</li><li>Digital gallery</li></ul><a class="package-link" href="packages.html">Explore packages ↗</a></article>
  </div>
</section>
{cta()}
"""

# ---------- About ----------
about = page_hero("01 / THE EXPERIENCE", "Step in.<br>Let yourself out.", "An enclosed photobooth for the moments that happen when the formalities are over.") + f"""
<section class="page-section">
  <div class="split">
    <div class="prose">
      <h2>A little space to be yourself.</h2>
      <p>The Strip is built around a simple idea: the best photographs happen when people forget they’re being photographed. Close the curtain, and the room disappears. The poses loosen. The real faces come out.</p>
      <p>It’s an enclosed booth — intimate, a little theatrical, and entirely yours for the moment. Step in with your favourite people, press the button, and let the strip tell the story.</p>
      <h3>Made to feel like part of the room.</h3>
      <p>Warm wood, soft light and a curtain that does its job. The Strip is designed to sit beautifully in a venue, not shout over it — and to feel like a small event of its own.</p>
      <h3>Keepsakes, not just photographs.</h3>
      <p>You leave with a printed strip in your hand and a digital copy to keep, share and look back on. Something tangible from a night that went by too quickly.</p>
      <a class="text-link" href="gallery.html">See the gallery <span>↗</span></a>
    </div>
    <div>
      <div class="image-strip" style="grid-template-columns:1fr;margin-top:0">
        <img src="assets/gallery-05.jpg" alt="A couple posing cheek to cheek in the booth" loading="lazy">
        <img src="assets/gallery-09.jpg" alt="Friends posing for a group photo" loading="lazy">
      </div>
    </div>
  </div>
  <div class="feature-grid">
    <div class="feature"><div class="num">01</div><h3>Enclosed by design.</h3><p>The curtain is the point. A little privacy makes room for a lot of personality.</p></div>
    <div class="feature"><div class="num">02</div><h3>Unlimited moments.</h3><p>Step in as many times as you like. The best strip is usually the one you didn’t plan.</p></div>
    <div class="feature"><div class="num">03</div><h3>Something to keep.</h3><p>Prints in hand, digital copies to share. The night leaves something behind.</p></div>
  </div>
</section>
{cta("Bring The Strip<br>to your event.")}
"""

# ---------- Gallery ----------
gallery = page_hero("THE GALLERY", "The gallery.", "Real people, real nights, and the faces that come out when the curtain closes.") + f"""
<section class="page-section tight">
  <div class="gallery-grid">{gallery_grid()}</div>
  {lightbox()}
  <p class="note">Printed strips from The Strip. More moments on the way.</p>
</section>
{cta()}
"""

# ---------- Packages ----------
packages = page_hero("PACKAGES", "Made for your<br>kind of night.", "Three starting points. Every booking is shaped around your event, your venue and the people in the room.") + f"""
<section class="page-section">
  <div class="package-grid">
    <article class="package-card">
      <div class="package-tag">01 / THE ESSENTIALS</div>
      <div class="package-name">The Classic</div>
      <div class="package-price">Tailored quote</div>
      <ul class="package-list">
        <li>Booth, delivery and setup</li>
        <li>Attendant on the night</li>
        <li>Unlimited sessions</li>
        <li>Printed strips to take home</li>
        <li>Digital gallery</li>
      </ul>
      <a class="package-link" href="contact.html">Enquire about The Classic ↗</a>
    </article>
    <article class="package-card">
      <div class="package-tag">02 / THE AFTER-PARTY</div>
      <div class="package-name">The Late Night</div>
      <div class="package-price">Tailored quote</div>
      <ul class="package-list">
        <li>Everything in The Classic</li>
        <li>Extra hours for the late crowd</li>
        <li>Custom print design</li>
        <li>Digital gallery</li>
      </ul>
      <a class="package-link" href="contact.html">Enquire about The Late Night ↗</a>
    </article>
    <article class="package-card">
      <div class="package-tag">03 / BRANDS &amp; IDEAS</div>
      <div class="package-name">The Something Else</div>
      <div class="package-price">Tailored quote</div>
      <ul class="package-list">
        <li>For launches and brand events</li>
        <li>Branded prints and backdrop</li>
        <li>Attendant on the night</li>
        <li>Digital gallery</li>
      </ul>
      <a class="package-link" href="contact.html">Enquire about The Something Else ↗</a>
    </article>
  </div>
  <div class="split" style="margin-top:64px">
    <div class="prose">
      <h2>Always included.</h2>
      <ul>
        <li>Delivery, setup and pack-down</li>
        <li>An attendant who knows the booth</li>
        <li>Unlimited sessions while we’re with you</li>
        <li>Printed strips and a digital gallery</li>
        <li>Props, if you want them</li>
      </ul>
      <h3>Add-ons, on request.</h3>
      <ul>
        <li>Extra hours</li>
        <li>A custom print design</li>
        <li>Branded backdrop or booth wrap</li>
        <li>Travel beyond the city</li>
      </ul>
    </div>
    <div class="prose">
      <h2>How pricing works.</h2>
      <p>Every event is different: the date, the venue, the hours and the details all shape the quote. Tell us what you’re planning and we’ll send a clear, tailored proposal — no packages forced into boxes.</p>
      <p>If you have a budget in mind, say so. We’d rather find the right version of The Strip for your night than send a number that doesn’t fit.</p>
      <a class="text-link" href="contact.html">Start an enquiry <span>↗</span></a>
    </div>
  </div>
  <p class="note">Prices are confirmed in your tailored quote. Full booking and cancellation terms are provided before you confirm.</p>
</section>
{cta()}
"""

# ---------- How it works ----------
how = page_hero("HOW IT WORKS", "From first message<br>to last photo.", "A simple process, with room for the details that make your event yours.") + f"""
<section class="page-section">
  <div class="steps-grid">
    <div class="step"><div class="num">01</div><h3>Enquire.</h3><p>Send us the date, the venue and a little about the occasion. We’ll check availability and come back with questions.</p></div>
    <div class="step"><div class="num">02</div><h3>We tailor.</h3><p>We shape the hours, the prints and the look around your event, then send a clear quote and booking details.</p></div>
    <div class="step"><div class="num">03</div><h3>We arrive.</h3><p>We deliver, set up and stay with the booth. You don’t have to manage a thing.</p></div>
  </div>
  <div class="split" style="margin-top:64px">
    <div class="prose">
      <h2>On the night.</h2>
      <p>The Strip arrives with its attendant, settles into the room, and stays ready. Guests step in, close the curtain, and take as many moments as they like.</p>
      <p>Prints come out on the night. A digital gallery follows, so the photographs don’t stay behind on a table.</p>
      <h3>Space and power.</h3>
      <p>The booth is compact, but every venue is different. We’ll confirm the footprint, access and a standard power point with you and your venue before the day.</p>
    </div>
    <div class="prose">
      <h2>Before the day.</h2>
      <p>Once the booking is confirmed, we’ll agree the arrival time, the setup window and the look of the prints. If you’re planning something unexpected, tell us early — that’s usually the fun part.</p>
      <h3>After the night.</h3>
      <p>You keep the prints. We’ll send the digital gallery so the photographs can travel further than the venue.</p>
      <a class="text-link" href="packages.html">See packages <span>↗</span></a>
    </div>
  </div>
</section>
{cta()}
"""

# ---------- FAQ ----------
faqs = [
    ("What is The Strip?", "The Strip is an enclosed photobooth. You step behind a curtain, take your photographs in private, and leave with a printed strip and a digital copy. It’s built for weddings, parties, launches and any night that deserves a record."),
    ("Is it really private?", "Yes. The booth is enclosed and the curtain closes behind you. That bit of privacy is exactly what makes the photographs feel different."),
    ("How much space do you need?", "The booth is compact, but the right spot depends on the venue and the flow of the room. Tell us about the space and we’ll confirm the footprint and access with you."),
    ("What about power?", "A standard power point is all we need. We’ll confirm the details with you and the venue before the event."),
    ("How many people fit?", "Enough for the moment — couples, friends, the whole wedding party. Step in, squeeze in, see what happens."),
    ("Do we get prints and digital copies?", "Yes. Guests take printed strips home on the night, and a digital gallery follows so the photographs can be shared and kept."),
    ("How long does setup take?", "We arrive ahead of the event and set up before guests need the booth. The exact window is agreed when we confirm the booking."),
    ("Do you travel?", "Tell us where the event is. Travel is quoted as part of your proposal, so there are no surprises."),
    ("Can we customise the prints?", "Yes. Print design, a branded backdrop and other details can be tailored to your event or brand."),
    ("Do you have an attendant?", "Yes. The booth comes with an attendant who sets up, stays with it and makes sure the night runs smoothly."),
    ("How do we book?", "Send an enquiry with your date and venue. We’ll confirm availability, shape the details and send a tailored quote. The booking is confirmed once the details and terms are agreed."),
    ("What is the cancellation policy?", "The booking terms, including cancellation, are set out clearly in your quote and booking agreement before you confirm."),
]
faq = page_hero("FAQ", "Good questions.", "The things people usually ask before they step behind the curtain.") + f"""
<section class="page-section">
  <div class="faq-list">
    {''.join(f'<details><summary>{esc(q)}</summary><div class="answer"><p>{esc(a)}</p></div></details>' for q, a in faqs)}
  </div>
  <p class="note">Still wondering about something? <a href="contact.html">Ask us directly</a>.</p>
</section>
{cta()}
"""

# ---------- Contact ----------
contact = page_hero("ENQUIRE", "Let’s make it<br>a date.", "Tell us a little about your event. We’ll come back with availability, questions and a tailored quote.") + f"""
<section class="page-section">
  <div class="contact-grid">
    <div>
      <form id="enquiry-form" class="form" novalidate>
        <input type="hidden" name="startedAt" id="startedAt">
        <div class="form-row">
          <label class="field">Your name<input name="name" autocomplete="name" required placeholder="Name &amp; surname"><span class="field-error" data-error-for="name" aria-live="polite"></span></label>
          <label class="field">Email address<input name="email" type="email" autocomplete="email" required placeholder="you@example.com"><span class="field-error" data-error-for="email" aria-live="polite"></span></label>
        </div>
        <div class="form-row">
          <label class="field">Phone <span class="muted">(optional)</span><input name="phone" type="tel" autocomplete="tel" placeholder="+27"></label>
          <label class="field">Event date<input name="date" type="date" required><span class="field-error" data-error-for="date" aria-live="polite"></span></label>
        </div>
        <div class="form-row">
          <label class="field">What’s the occasion?
            <select name="occasion">
              <option>Wedding</option>
              <option>Birthday / private party</option>
              <option>Brand / corporate event</option>
              <option>Something else</option>
            </select>
          </label>
          <label class="field">Where’s the party?<input name="location" required placeholder="Venue or town"><span class="field-error" data-error-for="location" aria-live="polite"></span></label>
        </div>
        <label class="field">Anything else?<textarea name="message" rows="4" placeholder="Tell us what you have in mind…"></textarea></label>
        <div class="honeypot" aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div>
        <label class="consent"><input type="checkbox" name="consent" required> I’m happy for The Strip to contact me about this enquiry. See the <a href="privacy.html">privacy policy</a>.</label>
        <span class="field-error" data-error-for="consent" aria-live="polite"></span>
        <div id="turnstile-slot" class="turnstile-slot"></div>
        <button class="submit" type="submit">Send enquiry <span>↗</span></button>
        <p class="form-status" id="form-status" aria-live="polite"></p>
      </form>
      <div id="form-success" class="hidden" role="status">
        <h2 style="font-size:40px;letter-spacing:-1.5px;margin:0 0 12px">Thank you.</h2>
        <p class="prose" style="max-width:520px">Your enquiry is with us. We’ll be in touch to talk about your event, availability and the details.</p>
      </div>
    </div>
    <aside class="contact-aside">
      <h3>Prefer to write directly?</h3>
      <p>Email us and we’ll take it from there.</p>
      <a class="email" href="mailto:{EMAIL}">{EMAIL}</a>
      <p>We read every enquiry ourselves. Tell us the date, the place and the kind of night you’re imagining.</p>
      <p class="note">By sending an enquiry you agree to our <a href="privacy.html">privacy policy</a>. We only use your details to respond to this enquiry.</p>
    </aside>
  </div>
</section>
"""

# ---------- Occasions ----------
def occasion(slug, eyebrow, heading, lede, paragraphs, bullets, images, cta_heading):
    paras = "".join(f"<p>{p}</p>" for p in paragraphs)
    bullets_html = "".join(f"<li>{b}</li>" for b in bullets)
    imgs = "".join(f'<img src="assets/{name}" alt="{esc(alt)}" loading="lazy">' for name, alt in images)
    return page_hero(eyebrow, heading, lede) + f"""
<section class="page-section">
  <div class="split">
    <div class="prose">
      {paras}
      <h3>What to expect.</h3>
      <ul>{bullets_html}</ul>
      <a class="text-link" href="packages.html">See packages <span>↗</span></a>
    </div>
    <div class="image-strip" style="grid-template-columns:1fr;margin-top:0">
      {imgs}
    </div>
  </div>
</section>
{cta(cta_heading)}
"""

weddings = occasion(
    "weddings", "01 / THE BIG DAY", "The big day.",
    "The photographs between the formal photographs — the ones that actually feel like your people.",
    [
        "The dress is pinned, the speeches are done, and the dance floor is starting to fill. That’s when The Strip comes into its own.",
        "Couples, plus-ones, grandparents, the friends who never pose for the camera — step behind the curtain and let the evening loosen up.",
        "Prints go home in pockets and handbags. The digital gallery keeps the rest of the night close.",
    ],
    ["An enclosed booth for private, playful moments", "Unlimited sessions through the night", "Printed strips and a digital gallery", "An attendant who keeps everything moving"],
    [("gallery-02.jpg", "A couple sharing a kiss in the booth"), ("gallery-05.jpg", "A couple posing cheek to cheek"), ("gallery-06.jpg", "A couple in front of the booth curtain")],
    "Bring The Strip<br>to the wedding."
)

parties = occasion(
    "parties", "02 / THE LATE NIGHT", "The late night.",
    "Birthdays, celebrations, and the friends who come alive when the curtain closes.",
    [
        "The best part of a party is rarely the part that was planned. It’s the group that squeezes into the booth, the faces nobody expected, the strip that ends up on the fridge.",
        "The Strip is made for that hour of the night. Step in, take your time, come back for more.",
        "No queue of strangers watching. Just your people, a curtain and a reason to be ridiculous.",
    ],
    ["Unlimited sessions while we’re with you", "Prints to take home", "A digital gallery for the group chat", "Props, if you want them"],
    [("gallery-03.jpg", "Four friends posing together"), ("gallery-07.jpg", "Four friends smiling for the camera"), ("gallery-09.jpg", "Friends posing for a group photo")],
    "Make a night<br>of it."
)

corporate = occasion(
    "corporate", "03 / THE SOMETHING ELSE", "The something else.",
    "Launches, brand moments and gatherings that deserve more than another photo of a room.",
    [
        "A launch, a conference, a brand anniversary — the moments people remember are the ones they took part in.",
        "The Strip gives guests a reason to step away from the canapés and into a moment of their own. Branded prints and a considered backdrop make it feel like part of the story, not a side attraction.",
        "We’ll work with you on the look, the prints and the details, and keep the booth running while you host the room.",
    ],
    ["Branded prints and a custom backdrop", "An attendant on the night", "Digital gallery for guests", "A look tailored to your brand"],
    [("gallery-04.jpg", "A guest posing in sunglasses"), ("gallery-08.jpg", "A couple making playful faces"), ("gallery-11.jpg", "Five friends in a black-and-white booth photo")],
    "Talk to us about<br>your event."
)

# ---------- Legal ----------
privacy = page_hero("PRIVACY", "Privacy, plainly.", "What we collect, why we collect it, and how to ask us to stop.") + f"""
<section class="page-section">
  <div class="legal">
    <p><strong>Last updated: 18 November 2026.</strong></p>
    <h2>Who we are</h2>
    <p>The Strip is a photobooth service operating in South Africa. For privacy questions, contact <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    <h2>What we collect</h2>
    <p>When you send an enquiry, we collect your name, email address, phone number if you provide it, event date, occasion, venue or town, and anything you choose to tell us in your message.</p>
    <p>If you use the booth, we process the photographs taken in it for the purpose of printing them and providing the digital gallery. Photographs may contain personal information and images of people.</p>
    <h2>Why we collect it</h2>
    <p>We use enquiry details to respond to you, prepare a quote and manage a booking. We use event photographs to provide the service you booked. We do not sell your personal information.</p>
    <h2>How long we keep it</h2>
    <p>Enquiry details are kept for as long as needed to respond and manage the relationship, and for reasonable business records afterwards. Photographs and galleries are kept for the period agreed for your event. Ask us if you want a specific retention period.</p>
    <h2>Who we share it with</h2>
    <p>We use service providers for hosting, email, payments and photo delivery where needed to run the service. We only share what is necessary for those services, and we do not sell data.</p>
    <h2>Your rights</h2>
    <p>Under South Africa’s Protection of Personal Information Act (POPIA), you may ask to access, correct or delete your personal information, or object to processing. Email <a href="mailto:{EMAIL}">{EMAIL}</a> and we will respond.</p>
    <h2>Cookies and analytics</h2>
    <p>This site does not currently use advertising cookies. If we add analytics, we will update this page and ask for consent where required.</p>
    <h2>Security</h2>
    <p>We take reasonable steps to protect the information we hold. No system is completely secure; please avoid sending sensitive information through the enquiry form.</p>
    <h2>Changes</h2>
    <p>We may update this policy as the service grows. The date at the top shows the latest version.</p>
  </div>
</section>
"""

terms = page_hero("TERMS", "The practical bits.", "Booking, payment and the things worth agreeing before the night.") + f"""
<section class="page-section">
  <div class="legal">
    <p><strong>Last updated: 18 November 2026.</strong> These are the general terms for The Strip. The specific details of your booking — date, hours, venue, quote and cancellation window — are set out in your booking agreement.</p>
    <h2>Quotes and bookings</h2>
    <p>An enquiry is not a booking. A booking is confirmed once the details, quote and booking terms are agreed and any required deposit is received. Dates are held only once confirmed.</p>
    <h2>Payment</h2>
    <p>Payment terms, including any deposit and the balance due date, are set out in your quote. Work outside the agreed scope may be quoted separately.</p>
    <h2>Cancellation and changes</h2>
    <p>The cancellation and rescheduling terms for your event are set out in your booking agreement. Tell us as early as possible if anything changes; we will always try to find a workable option.</p>
    <h2>Venue, space and power</h2>
    <p>You are responsible for confirming that the venue allows the booth, that the space and access are suitable, and that a standard power point is available. We will confirm the footprint and requirements with you before the event.</p>
    <h2>Setup and operation</h2>
    <p>We arrive within the agreed setup window and operate the booth for the agreed hours. Delays caused by the venue, access or power may affect the operating time.</p>
    <h2>Photographs and prints</h2>
    <p>We will make reasonable efforts to deliver the prints and digital gallery described in your booking. Print quantities and gallery details are confirmed in your quote.</p>
    <h2>Damage and liability</h2>
    <p>Please treat the booth and its props with care. You may be responsible for loss or damage caused by you or your guests. Our liability is limited to the amount paid for the affected booking, to the extent permitted by law.</p>
    <h2>Imagery</h2>
    <p>We may ask permission to share selected photographs from your event. We will not use identifiable images for marketing without consent.</p>
    <h2>Contact</h2>
    <p>Questions about these terms: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </div>
</section>
"""

not_found = """
<section class="not-found">
  <div class="eyebrow">404</div>
  <h1>This page stepped<br>behind the curtain.</h1>
  <p>It’s not here. The rest of The Strip is.</p>
  <a href="index.html">Back to the beginning ↗</a>
</section>
"""

# ---------- Build ----------
PAGES = [
    ("index", "The Strip — Behind the curtain. In the moment.", "An enclosed photobooth for weddings, parties and events. A little privacy, a lot of personality.", home, None, ""),
    ("about", "The experience — The Strip", "An enclosed photobooth built for the moments between the formal ones. Meet The Strip.", about, "about", ""),
    ("gallery", "Gallery — The Strip", "Real people, real nights, and the faces that come out when the curtain closes.", gallery, "gallery", ""),
    ("packages", "Packages — The Strip", "Tailored photobooth packages for weddings, parties and brand events. Every quote shaped around your night.", packages, "packages", ""),
    ("how-it-works", "How it works — The Strip", "From first enquiry to the last photograph: how The Strip works, from setup to digital gallery.", how, "how-it-works", ""),
    ("faq", "FAQ — The Strip", "Space, power, prints, travel and booking: the questions people ask before stepping behind the curtain.", faq, "faq", ""),
    ("contact", "Enquire — The Strip", "Tell us about your event. We’ll come back with availability and a tailored quote.", contact, "contact", ""),
    ("weddings", "Weddings — The Strip", "An enclosed photobooth for the moments between the formal photographs.", weddings, "about", ""),
    ("parties", "Parties — The Strip", "Birthdays, celebrations and the late-night moments worth keeping.", parties, "about", ""),
    ("corporate", "Corporate & brand events — The Strip", "A photobooth for launches, conferences and brand moments people take part in.", corporate, "about", ""),
    ("privacy", "Privacy — The Strip", "What we collect, why, and how to exercise your rights under POPIA.", privacy, None, ""),
    ("terms", "Terms — The Strip", "The practical terms for booking The Strip, from quotes and payments to venue requirements.", terms, None, ""),
]

for slug, title, description, content, active, extra in PAGES:
    html = layout(slug, title, description, content, active=active, head_extra=extra)
    (ROOT / f"{slug}.html").write_text(html, encoding="utf-8")

(ROOT / "404.html").write_text(
    layout("404", "Page not found — The Strip", "This page stepped behind the curtain.", not_found, noindex=True),
    encoding="utf-8"
)

sitemap_urls = "\n".join(
    f"  <url><loc>{SITE}/{'' if slug == 'index' else slug + '.html'}</loc><lastmod>2026-11-18</lastmod><changefreq>monthly</changefreq><priority>{'1.0' if slug == 'index' else '0.7'}</priority></url>"
    for slug, *_ in PAGES
)
(ROOT / "sitemap.xml").write_text(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_urls}\n</urlset>\n',
    encoding="utf-8"
)
(ROOT / "robots.txt").write_text(
    ("User-agent: *\nDisallow: /\n" if STAGING else f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n"),
    encoding="utf-8"
)
(ROOT / ".nojekyll").write_text("", encoding="utf-8")

print(f"Built {len(PAGES)} pages + 404")
