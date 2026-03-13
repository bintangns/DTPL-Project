# Destination Pages — Walkthrough

## What Was Built

The **Destinasi Wisata** section for the Desa Manud Jaya Django project:

- **Landing page** at `/destinasi/` — hero banner, 6 destination cards, ticket info, ecotourism commitment
- **6 Detail pages** at `/destinasi/<slug>/` — hero image, description, access info, facilities, sidebar with visit info
- **Navigation** — home page navbar, footer, and Wisata Alam card all link to destinations

## Files Changed

| Action | File |
|---|---|
| Modified | `DTPL/settings.py` — added `destinations` to `INSTALLED_APPS` |
| Modified | `DTPL/urls.py` — added `/destinasi/` route |
| Modified | `templates/base.html` — dynamic navbar active state + destination links |
| Modified | `home/templates/home/index.html` — Wisata Alam card link |
| Created | `destinations/urls.py` — list + detail URL patterns |
| Created | `destinations/views.py` — 6 destination data dicts + 2 views |
| Created | `destinations/templates/destinations/index.html` — landing page |
| Created | `destinations/templates/destinations/detail.html` — detail page |
| Created | `destinations/static/destinations/css/style.css` — all destination CSS |
| Created | `destinations/static/destinations/images/` — 6 generated images |

## Destinations

| Slug | Name | Difficulty |
|---|---|---|
| `air-terjun-kembar` | Air Terjun Kembar | Mudah |
| `bukit-savana-lestari` | Bukit Savana Lestari | Mudah hingga sedang |
| `danau-cermin` | Danau Cermin | Sangat mudah |
| `goa-karst-cemara` | Goa Karst Cemara | Sedang |
| `hutan-mangrove-bahari` | Hutan Mangrove Bahari | Mudah |
| `puncak-gunung-api-purba` | Puncak Gunung Api Purba | Menantang |

## Verification Results

All pages returned HTTP 200. Tested:

1. **Landing page** (`/destinasi/`) — hero, 3-column card grid, ticket info, ecotourism section ✅
2. **Detail pages** (e.g. `/destinasi/air-terjun-kembar/`) — hero image with badges, two-column layout, sidebar info cards ✅
3. **Navigation** — Navbar "Destinasi", footer "Destinasi Wisata", and Wisata Alam card all link correctly ✅
4. **Responsive** — 3-col → 2-col → 1-col breakpoints working ✅

## How to Run

```bash
cd "c:\Users\ahmad\Repo MTI\DTPL-Project\DTPL"
python manage.py runserver
```

Then visit:
- Landing: http://127.0.0.1:8000/destinasi/
- Detail example: http://127.0.0.1:8000/destinasi/air-terjun-kembar/
