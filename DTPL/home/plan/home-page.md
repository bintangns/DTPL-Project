# Desa Manud Jaya — Home Page (Static)

Build a visually rich static home page for Desa Manud Jaya served through Django templates, matching the provided mockup design.

## Project Root

```
c:\Users\ahmad\Repo MTI\DTPL-Project\DTPL\
```

## File Map — All Files to Modify or Create

| Action | Absolute Path |
|--------|---------------|
| MODIFY | `c:\Users\ahmad\Repo MTI\DTPL-Project\DTPL\DTPL\settings.py` |
| MODIFY | `c:\Users\ahmad\Repo MTI\DTPL-Project\DTPL\DTPL\urls.py` |
| MODIFY | `c:\Users\ahmad\Repo MTI\DTPL-Project\DTPL\home\views.py` |
| NEW | `c:\Users\ahmad\Repo MTI\DTPL-Project\DTPL\home\urls.py` |
| NEW | `c:\Users\ahmad\Repo MTI\DTPL-Project\DTPL\templates\base.html` |
| NEW | `c:\Users\ahmad\Repo MTI\DTPL-Project\DTPL\home\templates\home\index.html` |
| NEW | `c:\Users\ahmad\Repo MTI\DTPL-Project\DTPL\home\static\home\css\style.css` |
| NEW | `c:\Users\ahmad\Repo MTI\DTPL-Project\DTPL\home\static\home\images\hero-bg.jpg` *(generated)* |
| NEW | `c:\Users\ahmad\Repo MTI\DTPL-Project\DTPL\home\static\home\images\wisata-alam.jpg` *(generated)* |
| NEW | `c:\Users\ahmad\Repo MTI\DTPL-Project\DTPL\home\static\home\images\homestay.jpg` *(generated)* |
| NEW | `c:\Users\ahmad\Repo MTI\DTPL-Project\DTPL\home\static\home\images\produk-lokal.jpg` *(generated)* |

## Proposed Changes

---

### 1. Django Configuration

#### [MODIFY] settings.py
- Add `'home'` to `INSTALLED_APPS`
- Add project-level `templates/` directory to `TEMPLATES['DIRS']`
- Configure `STATICFILES_DIRS` to include project-level `static/` folder

#### [MODIFY] urls.py (project)
- Import `include` from `django.urls`
- Add `path('', include('home.urls'))` to serve home page at root `/`

---

### 2. Home App — Views & URLs

#### [MODIFY] views.py
- Add a `home` view function that renders `home/index.html`

#### [NEW] urls.py (home app)
- Define `urlpatterns` with `path('', views.home, name='home')`

---

### 3. Templates

#### [NEW] base.html
Shared base template containing:
- `<head>`: Google Fonts (Poppins), viewport meta, CSS block
- **Navbar**: logo text "Manud Jaya" (green) + links (Beranda, Destinasi, Homestay, Produk Lokal)
- `{% block content %}` for page-specific content
- **Footer** (3-column dark):
  - Col 1: Desa Manud Jaya — description
  - Col 2: Kontak — alamat, telepon, email
  - Col 3: Navigasi — Destinasi Wisata, Homestay, Produk Lokal
  - Copyright bar: © 2026 Desa Manud Jaya

#### [NEW] index.html
Extends `base.html`. Two main sections:

| Section | Elements |
|---------|----------|
| **Hero** | Full-viewport bg image, dark gradient overlay, "Desa Manud Jaya" title, tagline, description, green CTA button, animated scroll arrow |
| **Potensi Desa** | Centered heading + sub-text, 3 feature cards (Wisata Alam, Homestay Ramah Lingkungan, Produk Lokal Berkualitas) each with image, icon badge, title, paragraph, "Lihat Selengkapnya →" link |

---

### 4. Stylesheet

#### [NEW] style.css
Design tokens from mockup:

| Token | Value |
|-------|-------|
| Primary Green | `#2d6a4f` |
| Dark BG (footer) | `#1a1a2e` |
| Font | `'Poppins', sans-serif` |
| Hero overlay | `linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.55))` |
| Card radius | `12px` |
| Card shadow | `0 4px 20px rgba(0,0,0,0.08)` |

Responsive breakpoints: 1024px (tablet), 768px (mobile)

---

### 5. Images (AI-Generated)

| File | Description |
|------|-------------|
| `hero-bg.jpg` | Panoramic Indonesian village, rice terraces, tropical forest |
| `wisata-alam.jpg` | Tropical waterfall in green forest |
| `homestay.jpg` | Traditional Indonesian bamboo homestay |
| `produk-lokal.jpg` | Indonesian local products (coffee, chocolate) |

---

## Verification Plan

### Dev Server Check
```bash
cd "c:\Users\ahmad\Repo MTI\DTPL-Project\DTPL"
python manage.py runserver
```

### Visual Browser Comparison
- ✅ Navbar with logo + 4 links
- ✅ Full-screen hero with overlay, title, tagline, CTA button
- ✅ Scroll-down arrow animation
- ✅ 3-column feature cards with images and icon badges
- ✅ Dark footer with 3 columns + copyright
- ✅ Green color scheme and Poppins typography
