# Admin Panel — Documentation Plan

## Objective

Menyediakan panel admin berbasis web untuk Pokdarwis/Karang Taruna Desa Manud Jaya agar operasional pengelolaan homestay, produk lokal, dan pemesanan dapat dilakukan secara digital melalui satu dashboard terpusat.

## User Story

**Sebagai** admin pengelola desa (Pokdarwis/Karang Taruna),  
**Saya ingin** memiliki dashboard untuk mengelola data homestay, produk, dan pemesanan  
**Agar** operasional dapat dilakukan secara digital.

### Sub-User Stories

| ID | User Story | Priority |
|----|-----------|----------|
| AP-01 | Sebagai admin, saya ingin login ke panel admin dengan username dan password | Must |
| AP-02 | Sebagai admin, saya ingin melihat sidebar navigasi untuk berpindah antar halaman | Must |
| AP-03 | Sebagai admin, saya ingin melihat ringkasan statistik di dashboard utama | Must |
| AP-04 | Sebagai admin, saya ingin melihat daftar homestay dalam format kartu | Must |
| AP-05 | Sebagai admin, saya ingin mengelola produk lokal (CRUD) | Must |
| AP-06 | Sebagai admin, saya ingin melihat daftar pemesanan homestay | Must |
| AP-07 | Sebagai admin, saya ingin melihat dan mengelola pemesanan produk | Must |
| AP-08 | Sebagai admin, saya ingin logout dari panel admin | Must |
| AP-09 | Sebagai admin, saya ingin bisa kembali ke website publik via link "Lihat Website" | Should |
| AP-10 | Sebagai pengunjung, saya ingin melihat tombol "Login Admin" di navbar website publik untuk masuk ke panel admin | Should |

## Detailed Changes

### Public Navbar Login Button
- Add "Login Admin" button to public website navbar (top-right)
- When admin is logged in, button changes to "Admin Dashboard" linking to `/admin/dashboard/`
- When not logged in, button links to `/admin/` (login page)

### Layout Overhaul
- **Before**: Top navbar with horizontal navigation + hero section + feature cards
- **After**: Fixed left sidebar (240px) + top header bar + content area
- Sidebar items: Dashboard, Homestay, Produk Lokal, Pemesanan Homestay, Pemesanan Produk
- Top header: Logo, "Lihat Website" link, admin name, logout button

### Shared Template System
- New `base.html` template in `adminpanel/templates/adminpanel/`
- All admin pages across all apps extend this base template
- Active sidebar state managed via context variable `active_nav`

### Pages (5 total)
1. **Dashboard** — Statistics overview (handled by `dashboard` app)
2. **Homestay** — Card grid display (handled by `homestays` app, hardcoded data)
3. **Produk Lokal** — Product CRUD cards (handled by `products` app, real DB data)
4. **Pemesanan Homestay** — Booking table (handled by `homestays` app, hardcoded data)
5. **Pemesanan Produk** — Order table (handled by `products` app, real DB data)

### Scope Exclusions
- No new database models created
- No homestay CRUD (another developer handles this)
- Homestay and booking data are hardcoded in views

## Definition of Done

- [ ] Admin can login at `/admin/` and see the new sidebar layout
- [ ] All 5 sidebar navigation links work and route to correct pages
- [ ] Active sidebar item is highlighted on each page
- [ ] "Lihat Website" link navigates to the public homepage
- [ ] Logout button clears session and redirects to login
- [ ] Dashboard page shows statistics cards and recent order sections
- [ ] Homestay page shows card grid with hardcoded data
- [ ] Produk Lokal page shows product cards with working CRUD
- [ ] Pemesanan Homestay page shows table with hardcoded booking data
- [ ] Pemesanan Produk page shows table with real order data
- [ ] All pages use consistent styling matching the design mockups
- [ ] Design uses Poppins font, green primary color scheme, rounded cards
