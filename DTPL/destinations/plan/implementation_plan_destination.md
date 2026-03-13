# Destination Pages — Implementation Plan

Build the **Destinasi Wisata** landing page and 6 individual destination detail pages for the Desa Manud Jaya Django project, following the existing `home` app patterns and the provided mockup screenshots.

## Proposed Changes

### 1. Django Configuration

#### [MODIFY] `DTPL/settings.py`
- Add `'destinations'` to `INSTALLED_APPS`

#### [MODIFY] `DTPL/urls.py`
- Add `path('destinasi/', include('destinations.urls'))`

---

### 2. Home Page — Navigation Connections

#### [MODIFY] `templates/base.html`
- Navbar "Destinasi" link: `href="#"` → `href="{% url 'destinations:list' %}"`
- Footer "Destinasi Wisata" link: `href="#"` → `href="{% url 'destinations:list' %}"`
- Make active nav link dynamic via template blocks

#### [MODIFY] `home/templates/home/index.html`
- "Wisata Alam" card link: `href="#"` → `href="{% url 'destinations:list' %}"`

> **Note:** No content/layout changes to the home page. Only link updates.

---

### 3. Destinations App — Backend

#### [NEW] `destinations/urls.py`
- `app_name = 'destinations'`
- `path('', views.destination_list, name='list')` → landing page
- `path('<slug:slug>/', views.destination_detail, name='detail')` → detail page

#### [MODIFY] `destinations/views.py`
- Define `DESTINATIONS` list of dicts with all content from plan files (static data, no database)
- `destination_list(request)` → renders landing page
- `destination_detail(request, slug)` → finds by slug, 404 if not found

| Slug | Name |
|---|---|
| `air-terjun-kembar` | Air Terjun Kembar |
| `bukit-savana-lestari` | Bukit Savana Lestari |
| `danau-cermin` | Danau Cermin |
| `goa-karst-cemara` | Goa Karst Cemara |
| `hutan-mangrove-bahari` | Hutan Mangrove Bahari |
| `puncak-gunung-api-purba` | Puncak Gunung Api Purba |

---

### 4. Destinations App — Templates

#### [NEW] `destinations/templates/destinations/index.html`
Extends `base.html`. Sections:
1. Hero banner — green gradient with "Destinasi Wisata" heading
2. Destination cards grid — 3-column responsive, each with image, badges, meta, "Lihat Detail" link
3. Tiket Masuk section — Rp 20.000 info card
4. Komitmen Ecotourism section

#### [NEW] `destinations/templates/destinations/detail.html`
Extends `base.html`. Sections:
1. Back navigation — "← Kembali ke Daftar Destinasi"
2. Hero image with overlay badges/title
3. Two-column layout: left (description, access, facilities) + right sidebar (info card, ecotourism card)

---

### 5. Destinations App — CSS

#### [NEW] `destinations/static/destinations/css/style.css`
Reuses `:root` CSS variables from home page. Covers:
- Destination hero, cards grid, ticket info, ecotourism section
- Detail hero, two-column layout, sidebar cards
- Responsive breakpoints (1024px, 768px, 480px)

---

### 6. Image Assets

#### [NEW] 6 images in `destinations/static/destinations/images/`
- `air-terjun-kembar.jpg` — Twin waterfall in tropical forest
- `bukit-savana-lestari.jpg` — Savanna hills with sunset
- `danau-cermin.jpg` — Mirror lake with clear water
- `goa-karst-cemara.jpg` — Limestone cave with stalactites
- `hutan-mangrove-bahari.jpg` — Mangrove forest boardwalk
- `puncak-gunung-api-purba.jpg` — Ancient volcano peak at sunrise

---

## Verification

1. Home page → "Destinasi" link navigates to `/destinasi/`
2. Landing page → 6 cards visible with images, badges, links
3. Detail pages → All 6 slugs load with full content
4. 404 handling → Invalid slug returns 404
5. Responsive → Check at 1024px, 768px, 480px
