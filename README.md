# Anitha Techsolutions website

Static, SEO-ready company website with a 3D hero, built from `build.py`.

## Edit and build

1. Edit content and settings in `build.py`:
   - `SITE_URL` — your real domain (required before publishing; used for canonical links, sitemap, social cards)
   - `EMAIL`, `APP_STORE_URL` (Odoo Apps Store link for Sale Order Split once published)
   - `SERVICES`, `MOBILE_USECASES`, `HOME_FAQ`, `POSTS` (blog articles) …
2. Styles: `src/css/style.css` · 3D hero: `src/js/hero3d.js` · interactions: `src/js/main.js`
3. Build: `python3 build.py` → the finished site is written to `public/`.

## Preview locally

```
cd public && python3 -m http.server 8765
```
Open http://127.0.0.1:8765 (opening the files directly works too, but "install as app" needs http).

## Publish

Live at **https://anithatechsolutions.github.io** (GitHub Pages).

Deployment is automatic: push to `main` and the GitHub Actions workflow
(`.github/workflows/deploy.yml`) runs `build.py` and publishes `public/`.
`public/` is generated, so it is not committed.

- Submit `https://anithatechsolutions.github.io/sitemap.xml` in Google Search Console and Bing Webmaster Tools.
- Custom domain later: set `SITE_URL` in `build.py`, add the domain under repo Settings → Pages, and point DNS at GitHub.

## What's included

- Pages: Home, Odoo Services, Mobile App Development, Odoo Apps, About, Blog (3 articles), Contact
- SEO: unique titles/descriptions, canonical URLs, Open Graph/Twitter cards, JSON-LD
  (Organization, WebSite, FAQPage, Service, SoftwareApplication, BlogPosting, BreadcrumbList),
  sitemap.xml, robots.txt, semantic headings, alt text on every image
- Installable as a mobile app (PWA): web manifest, service worker, offline page, install prompt
- Brand: logos, favicons and colours from the Anitha Techsolutions brand kit (Montserrat,
  Navy #0E1B33, Signal Blue #2F5BEA, Slate #64748B, Gold #C6A15B)
