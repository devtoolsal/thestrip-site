# The Strip — website + operations console

Static website and operations console for The Strip photobooth. Built with plain HTML, CSS and JavaScript. The visual language and palette come directly from the client's existing site.

## Pages

- `index.html` — home
- `about.html` — the experience
- `gallery.html` — full gallery with lightbox
- `packages.html` — packages and pricing approach
- `how-it-works.html` — process and logistics
- `faq.html` — common questions
- `contact.html` — booking enquiry form
- `weddings.html`, `parties.html`, `corporate.html` — occasion pages
- `privacy.html`, `terms.html` — legal templates
- `404.html` — not found

`admin/` contains the operations console (fleet, sites, enquiries, OTA, orders, plans, audit).

## Brand

- Paper `#F4F3EF`
- Ink `#232320`
- Muted `#77756E` (small text uses the darker `--muted-ink` for contrast)
- Line `#CECDC6`
- CTA band `#DEDED4`
- Placeholder `#D6D2CB`
- Rust `#9E5538`
- Typeface: DM Sans
- Wordmark: “The Strip”, title case, tight tracking, no dot

## Local preview

```bash
python3 build.py          # regenerate the pages after editing content
node build-assets.mjs     # regenerate favicon/apple touch/OG image
python3 -m http.server 8080
```

Open `http://localhost:8080/` and `http://localhost:8080/admin/`.

## API

The site is static. The booking form and admin console call the API configured in `js/config.js`:

```js
window.THESTRIP_API_BASE = "https://…/v1";
```

Currently this points at the staging tunnel. The website booking form falls back to a pre-filled email if the API is unavailable. The admin console requires the admin token.

The API lives in `thestrip/apps/api` and is deployed separately. For production, point `THESTRIP_API_BASE` at the production API and update the canonical/sitemap domain.

## Live staging

- Website: https://devtoolsal.github.io/thestrip-site/
- Admin: https://devtoolsal.github.io/thestrip-site/admin/
- Repository: https://github.com/devtoolsal/thestrip-site

## Deploy

This folder is the GitHub Pages document root. Push `main` and enable Pages on the repository. No build step is required for the deployed output; `build.py` and `build-assets.mjs` are source tooling.

The live site at `www.thestripphotobooth.co.za` is not touched by this repository. Migration requires owner approval and DNS/hosting access.

## Still to confirm with the client

- Real package pricing and inclusions.
- Phone/WhatsApp, social links, service area and travel terms.
- Final booking/cancellation policy and legal entity details.
- Higher-resolution gallery originals.
- Production API host and domain cutover.
