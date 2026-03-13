# Walkthrough — Desa Manud Jaya Home Page

## What Was Built
A visually rich static home page for **Desa Manud Jaya** served through Django templates, matching the provided mockup design.

## Screenshots

````carousel
![Hero Section — navbar, background image, title, tagline, CTA button, scroll arrow](C:\Users\ahmad\.gemini\antigravity\brain\83179f3e-04fc-4e37-ad4d-2879bd27f1c7\hero_section_1772860654931.png)
<!-- slide -->
![Cards & Footer — feature cards section and dark footer with 3 columns](C:\Users\ahmad\.gemini\antigravity\brain\83179f3e-04fc-4e37-ad4d-2879bd27f1c7\cards_and_footer_1772860682040.png)
````

## Files Changed

| Action | File |
|--------|------|
| MODIFY | [settings.py](file:///c:/Users/ahmad/Repo%20MTI/DTPL-Project/DTPL/DTPL/settings.py) — registered `home` app, template dir, static files |
| MODIFY | [urls.py](file:///c:/Users/ahmad/Repo%20MTI/DTPL-Project/DTPL/DTPL/urls.py) — added `home.urls` at root |
| MODIFY | [views.py](file:///c:/Users/ahmad/Repo%20MTI/DTPL-Project/DTPL/home/views.py) — added `home` view |
| NEW | [urls.py](file:///c:/Users/ahmad/Repo%20MTI/DTPL-Project/DTPL/home/urls.py) — home app URL config |
| NEW | [base.html](file:///c:/Users/ahmad/Repo%20MTI/DTPL-Project/DTPL/templates/base.html) — shared nav + footer |
| NEW | [index.html](file:///c:/Users/ahmad/Repo%20MTI/DTPL-Project/DTPL/home/templates/home/index.html) — hero + cards |
| NEW | [style.css](file:///c:/Users/ahmad/Repo%20MTI/DTPL-Project/DTPL/home/static/home/css/style.css) — full stylesheet |
| NEW | [home-page.md](file:///c:/Users/ahmad/Repo%20MTI/DTPL-Project/DTPL/home/plan/home-page.md) — implementation plan |
| NEW | 4 AI-generated images in `home/static/home/images/` |

## Verification Results

- ✅ Django dev server started without errors at `http://127.0.0.1:8000/`
- ✅ Navbar: transparent on hero, solid on scroll, logo + 4 navigation links
- ✅ Hero: full-viewport background, gradient overlay, title, tagline, CTA button, animated scroll arrow
- ✅ Cards section: 3 feature cards with images, green icon badges, text, and links
- ✅ Footer: dark background, contact info, navigation links, copyright bar
- ✅ Green color scheme (#2d6a4f) and Poppins typography throughout

## How to Run

```bash
cd "c:\Users\ahmad\Repo MTI\DTPL-Project\DTPL"
py manage.py runserver
```
Then open `http://127.0.0.1:8000/` in your browser.
