# Dashboard Section — Documentation Plan

## Objective

Menyediakan halaman dashboard utama yang menampilkan ringkasan statistik platform wisata Desa Manud Jaya, termasuk total pendapatan, jumlah homestay, jumlah produk, jumlah transaksi, status pemesanan, dan daftar pemesanan terbaru.

## User Story

**Sebagai** admin pengelola desa,  
**Saya ingin** melihat ringkasan statistik platform wisata di satu halaman  
**Agar** saya dapat memantau kondisi operasional secara cepat tanpa harus membuka setiap halaman.

### Sub-User Stories

| ID | User Story | Priority |
|----|-----------|----------|
| DB-01 | Sebagai admin, saya ingin melihat total pendapatan dari semua transaksi | Must |
| DB-02 | Sebagai admin, saya ingin melihat jumlah homestay yang terdaftar | Must |
| DB-03 | Sebagai admin, saya ingin melihat jumlah produk yang tersedia | Must |
| DB-04 | Sebagai admin, saya ingin melihat jumlah total transaksi (homestay + produk) | Must |
| DB-05 | Sebagai admin, saya ingin melihat status pemesanan homestay (pending, dikonfirmasi, total) | Must |
| DB-06 | Sebagai admin, saya ingin melihat status pemesanan produk (pending, dikonfirmasi, total) | Must |
| DB-07 | Sebagai admin, saya ingin melihat 5 pemesanan homestay terbaru | Should |
| DB-08 | Sebagai admin, saya ingin melihat 5 pemesanan produk terbaru | Should |
| DB-09 | Sebagai admin, saya ingin link "Lihat Semua Pemesanan" untuk navigasi ke halaman pemesanan | Should |

## Detailed Changes

### App Structure
The `dashboard` Django app handles the dashboard page:
- `dashboard/views.py` — `dashboard_home` view gathers all statistics
- `dashboard/urls.py` — URL pattern registered under `/admin/dashboard/`
- `dashboard/templates/dashboard/home.html` — extends `adminpanel/base.html`

### Data Sources
| Stat | Source | Method |
|------|--------|--------|
| Total Pendapatan | `ProductOrder` (confirmed) | `aggregate(Sum('total'))` on confirmed orders |
| Total Homestay | Hardcoded list | `len(homestays)` |
| Total Produk | `Product` model | `Product.objects.count()` |
| Total Transaksi | `ProductOrder` + hardcoded bookings | Count sum |
| Homestay booking stats | Hardcoded | Filter by status field |
| Product order stats | `ProductOrder` model | `.filter(status=...).count()` |
| Recent homestay bookings | Hardcoded list | First 5 items |
| Recent product orders | `ProductOrder` model | `.order_by('-created_at')[:5]` |

### UI Components

#### Row 1: Stat Cards (4 cards)
| Card | Icon | Color | Value |
|------|------|-------|-------|
| Total Pendapatan | 💰 | Green gradient bg | `Rp X.XXX.XXX` |
| Total Homestay | 🏠 | Light blue icon | Count |
| Total Produk | 📦 | Light orange icon | Count |
| Total Transaksi | 👥 | Light purple icon | Count + detail text |

#### Row 2: Status Sections (2 columns)
- **Status Pemesanan Homestay**: Pending count, Dikonfirmasi count, Total, "Lihat Semua Pemesanan →" link
- **Status Pemesanan Produk**: Same structure for product orders

#### Row 3: Recent Orders (2 columns)
- **Pemesanan Homestay Terbaru**: List items with name, homestay, status badge, price
- **Pemesanan Produk Terbaru**: List items with name, product, date, status badge, price

### Migration from `adminpanel`
- The current dashboard view is in `adminpanel/views.py` as `admin_home`
- This will be moved to `dashboard/views.py` as `dashboard_home`
- The `adminpanel` URL `path('dashboard/', ...)` will route to `dashboard` app instead
- The `adminpanel` app retains login/logout functionality only

## Definition of Done

- [ ] Dashboard page loads at `/admin/dashboard/` after login
- [ ] Sidebar "Dashboard" item is highlighted (active state)
- [ ] 4 stat cards display correctly with icons and formatted numbers
- [ ] Total Pendapatan shows sum of confirmed product orders
- [ ] Total Homestay shows count from hardcoded data
- [ ] Total Produk shows real count from Product model
- [ ] Total Transaksi shows combined count
- [ ] Status Pemesanan Homestay section shows pending/confirmed/total
- [ ] Status Pemesanan Produk section shows pending/confirmed/total with real data
- [ ] "Lihat Semua Pemesanan" links navigate to respective pemesanan pages
- [ ] Pemesanan Homestay Terbaru shows up to 5 hardcoded bookings with status badges
- [ ] Pemesanan Produk Terbaru shows up to 5 real orders with status badges
- [ ] All currency values are formatted with "Rp" prefix and thousand separators
- [ ] Page renders correctly on desktop (1280px+)
