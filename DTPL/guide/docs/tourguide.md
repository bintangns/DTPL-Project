# Rencana Implementasi: Modul Tour Guide & Pemesanan Paket Wisata

> Dokumen ini merupakan **blueprint teknis** yang mendetailkan langkah-langkah implementasi untuk inisialisasi modul `guide` (Pemandu Wisata), pembuatan model `TourPackage` & `PackageBooking`, serta integrasi ke **destinations detail page** dan **admin dashboard**. Semua pola desain (model, view, form, email, template, sidebar) mengikuti konvensi yang sudah ada pada modul `homestays` dan `products`.

---

## 1. Ringkasan Produk

| Item | Detail |
|---|---|
| **User Story** | Sebagai calon Wisatawan, saya ingin memilih tanggal, jenis paket, dan kategori kewarganegaraan, sehingga saya mendapatkan paket harga yang sesuai dan pemandu yang bisa berkomunikasi dengan bahasa yang saya kuasai. |
| **Product Goal** | Penguatan Tata Kelola Berbasis Data |
| **Product Goal Statement** | Pengelola Desa Wisata dapat mengelola data wisata secara digital, mengambil keputusan berdasarkan laporan analitik platform, dan pemberdayaan pemuda lokal (Karang Taruna) sebagai garda terdepan dalam menjaga kelestarian budaya, memberikan edukasi berkualitas, dan memastikan keamanan wisatawan lintas negara demi pertumbuhan ekonomi desa yang berkelanjutan. |
| **Metrik Keberhasilan** | ≥ 10 pemuda terdaftar sebagai pemandu wisata |

---

## 2. Struktur Data (Models)

### 2.1 `guide/models.py` — Model `Guide`

| Field | Type | Keterangan |
|---|---|---|
| `name` | CharField(150) | Nama lengkap pemandu |
| `slug` | SlugField(unique) | Auto-generate dari `name`, pola sama dgn `Homestay.slug` |
| `category` | CharField(20, choices) | `'lokal'` atau `'internasional'` |
| `languages` | CharField(255) | Contoh: `"Indonesia, Sunda"` atau `"Indonesia, English, Japanese"`. Pisah koma. |
| `profile_picture` | ImageField(`upload_to='guides/'`) | Foto pemandu, upload ke `media/guides/` |
| `phone_number` | CharField(30) | Nomor WA/telepon |
| `email` | EmailField | Untuk kirim notifikasi booking |
| `bio` | TextField(blank) | Deskripsi singkat pengalaman |
| `is_available` | BooleanField(default=True) | Status ketersediaan umum (master toggle) |
| `created_at` | DateTimeField(auto_now_add) | Timestamp pendaftaran |

Properti helper:
- `languages_list` → split koma menjadi list, *pola sama* dgn `Destination.features_list`.

### 2.2 `guide/models.py` — Model `TourPackage`

| Field | Type | Keterangan |
|---|---|---|
| `destination` | ForeignKey(`Destination`, CASCADE, related_name=`'tour_packages'`) | Relasi ke destinasi |
| `name` | CharField(200) | Nama paket, contoh: "Paket Sunrise Savana" |
| `slug` | SlugField(unique, blank) | Auto-generate |
| `description` | TextField | Deskripsi detail paket |
| `itinerary` | TextField | Agenda kegiatan, bisa berisi bullet points |
| `price_local` | DecimalField(12,2) | Harga wisatawan lokal (IDR) |
| `price_international` | DecimalField(12,2) | Harga wisatawan mancanegara (IDR) |
| `image_url` | URLField(blank) | Foto paket wisata |
| `duration` | CharField(50) | Contoh: "4 Jam", "Full Day" |
| `max_participants` | PositiveIntegerField(default=10) | Batas peserta per sesi |
| `is_active` | BooleanField(default=True) | Toggle aktif/nonaktif |
| `created_at` | DateTimeField(auto_now_add) | - |

### 2.3 `guide/models.py` — Model `PackageBooking`

Mengadopsi pola dari `HomestayBooking` (`homestays/models.py` L46-94):

| Field | Type | Keterangan |
|---|---|---|
| `tour_package` | ForeignKey(`TourPackage`, CASCADE, related_name=`'bookings'`) | Paket yang dipesan |
| `guide` | ForeignKey(`Guide`, SET_NULL, null, blank, related_name=`'bookings'`) | Pemandu teralokasi |
| `customer_name` | CharField(150) | Nama pemesan |
| `email` | EmailField | Email pemesan |
| `phone_number` | CharField(30) | WA/Telepon |
| `tourist_category` | CharField(20, choices) | `'lokal'` atau `'mancanegara'` |
| `tour_date` | DateField | Tanggal wisata |
| `start_time` | TimeField | Jam mulai kegiatan |
| `num_participants` | PositiveIntegerField(default=1) | Jumlah peserta |
| `total_price` | DecimalField(12,2) | Dihitung otomatis berdasarkan `tourist_category` × `num_participants` |
| `payment_proof` | ImageField(`upload_to='payment_proofs/'`, blank, null) | *Pola sama* dgn `HomestayBooking.payment_proof` |
| `notes` | TextField(blank) | Catatan tambahan |
| `status` | CharField(20, choices, default=`'pending'`) | Pending / Confirmed / Completed / Cancelled |
| `created_at` | DateTimeField(auto_now_add) | - |

**`save()` override**: Auto-hitung `total_price` = `price_local * num_participants` jika lokal, atau `price_international * num_participants` jika mancanegara. *Pola sama* dgn `HomestayBooking.save()`.

---

## 3. File yang Perlu Dibuat / Dimodifikasi

### 3.1 File BARU di `guide/`

| # | File | Tujuan |
|---|---|---|
| 1 | `guide/__init__.py` | Package init |
| 2 | `guide/apps.py` | AppConfig `guide` |
| 3 | `guide/models.py` | Model `Guide`, `TourPackage`, `PackageBooking` |
| 4 | `guide/forms.py` | `GuideForm`, `TourPackageForm`, `PackageBookingForm` (public), form widget flatpickr |
| 5 | `guide/views.py` | Public views: `tour_package_list`, `tour_package_detail`, `package_booking_create`, `booking_success`. Admin views: CRUD Guide, CRUD TourPackage, BookingList, BookingUpdateStatus |
| 6 | `guide/urls.py` | Public URL patterns (`app_name='guide'`) |
| 7 | `guide/admin_urls.py` | Admin URL patterns (`app_name='guide_admin'`) |
| 8 | `guide/admin.py` | Register models ke Django Admin sebagai backup |
| 9 | `guide/migrations/0001_initial.py` | Auto-generated via `makemigrations` |

### 3.2 Templates BARU di `guide/templates/guide/`

| # | Template | Tujuan |
|---|---|---|
| 1 | `tour_packages_section.html` | Partial include di halaman detail destinasi — menampilkan daftar paket wisata. User klik CTA → modal/form booking |
| 2 | `booking_form_modal.html` | Modal form pemesanan paket wisata (mirip booking modal di `homestay_detail.html`) |
| 3 | `booking_success.html` | Halaman konfirmasi setelah booking berhasil |
| 4 | `admin_guide_list.html` | Admin: daftar pemandu wisata (extends `adminpanel/base.html`) |
| 5 | `admin_guide_form.html` | Admin: form tambah/edit pemandu (extends `adminpanel/base.html`) |
| 6 | `admin_guide_delete.html` | Admin: konfirmasi hapus pemandu |
| 7 | `admin_package_list.html` | Admin: daftar paket wisata |
| 8 | `admin_package_form.html` | Admin: form tambah/edit paket |
| 9 | `admin_booking_list.html` | Admin: daftar pemesanan paket wisata masuk (extends `adminpanel/base.html`, pola mirip `homestays/admin_booking_list.html`) |

### 3.3 Static files BARU

| # | File | Tujuan |
|---|---|---|
| 1 | `guide/static/guide/css/style.css` | Styling untuk section paket wisata di detail destinasi & modal booking |

### 3.4 File YANG DIMODIFIKASI (Existing)

| # | File | Perubahan |
|---|---|---|
| 1 | `DTPL/settings.py` | Tambah `'guide'` ke `INSTALLED_APPS` |
| 2 | `DTPL/urls.py` | Tambah `path('admin/guide/', include('guide.admin_urls'))` dan `path('paket-wisata/', include('guide.urls'))` |
| 3 | `destinations/templates/destinations/detail.html` | Tambahkan `{% include 'guide/tour_packages_section.html' %}` di bawah section Aktivitas, sebelum review |
| 4 | `destinations/views.py` | Di `destination_detail()`: query `TourPackage.objects.filter(destination=destination, is_active=True)` dan pass ke context |
| 5 | `adminpanel/templates/adminpanel/base.html` | Tambahkan 2 sidebar link baru: "Pemandu Wisata" (`guide_admin:guide_list`) dan "Pemesanan Paket Wisata" (`guide_admin:booking_list`) |
| 6 | `dashboard/views.py` | Tambahkan statistik paket wisata: `total_guides`, `total_package_bookings`, `package_bookings_pending`, dll |
| 7 | `dashboard/templates/dashboard/home.html` | Tambahkan card statistik pemandu wisata & section pemesanan paket terbaru |
| 8 | `guide/migrations/0002_seed_guides.py` | Data migration: 10+ pemandu wisata + beberapa paket wisata contoh |

---

## 4. Detail Implementasi Per-Fitur

### 4.1 Inisialisasi App Django `guide`

Karena folder `guide/` sudah ada (berisi `docs/`), kita **tidak** menggunakan `startapp`. Sebaliknya, kita buat file-file Django secara manual.

**`guide/apps.py`**:
```python
from django.apps import AppConfig

class GuideConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'guide'
    verbose_name = 'Tour Guide & Paket Wisata'
```

**`DTPL/settings.py`** — tambahkan ke `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ... existing ...
    'guide',
]
```

### 4.2 CRUD Admin Pemandu Wisata

Mengikuti pola `homestays` admin CRUD:
- **List**: Tabel pemandu + statistik (total pemandu, lokal, internasional, available)
- **Create/Edit**: Form dengan fields: foto, nama, kategori (dropdown), bahasa, bio, email, telpon, status
- **Delete**: Konfirmasi hapus (POST, pola sama dgn `admin_homestay_delete`)

### 4.3 Halaman Detail Destinasi — Section Paket Wisata

Di halaman `destinations/detail.html`, setelah section Aktivitas, tambahkan section baru yang menampilkan:
1. **Katalog paket wisata** terkait destinasi tersebut (card layout)
2. Setiap card berisi: gambar, nama paket, durasi, deskripsi singkat, harga (Lokal/Internasional), dan tombol **"Pesan Paket"**
3. Tombol "Pesan Paket" membuka **modal booking** (pola sama dgn homestay booking modal di `homestay_detail.html`)

### 4.4 Form Pemesanan Paket Wisata (Modal)

Pola mengikuti `homestay_detail.html` L174-215:
- **Date Picker & Time Picker**: Menggunakan `flatpickr` (sudah ada di project, lihat `homestay_detail.html` L9, L219). `minDate: "today"` untuk disable tanggal lampau.
- **Radio Button**: Kategori wisatawan "Lokal" atau "Mancanegara"
- **Harga otomatis**: JavaScript menghitung + menampilkan harga berdasarkan pilihan kategori × jumlah peserta
- **Fields**: Nama, Email, Telepon, Tanggal, Jam Mulai, Kategori Wisatawan, Jumlah Peserta, Bukti Pembayaran, Catatan

### 4.5 Guide Matching System

Di `views.py` → `package_booking_create()`:
```python
# 1. Filter pemandu yang available
available_guides = Guide.objects.filter(is_available=True)

# 2. Jika wisatawan Mancanegara → wajib pemandu Internasional
if tourist_category == 'mancanegara':
    available_guides = available_guides.filter(category='internasional')

# 3. Exclude pemandu yang sudah ada booking confirmed di tanggal tersebut
booked_guide_ids = PackageBooking.objects.filter(
    tour_date=tour_date,
    status__in=['confirmed', 'pending']
).values_list('guide_id', flat=True)
available_guides = available_guides.exclude(id__in=booked_guide_ids)

# 4. Alokasi pemandu pertama yang tersedia (atau random)
guide = available_guides.first()
```

### 4.6 Halaman Ringkasan / Booking Success

Setelah submit booking berhasil, redirect ke halaman sukses yang menampilkan:
- Detail paket wisata
- Tanggal & jam kegiatan
- Kategori wisatawan & total harga
- **Profil singkat pemandu**: Foto, nama, kategori, bahasa yang dikuasai

### 4.7 Notifikasi Email (Brevo API)

Mengikuti **pola persis** dari `homestays/views.py` L16-57 (`send_order_status_email`):
- Copy helper `send_order_status_email` ke `guide/views.py` (atau refactor ke shared util)
- Kirim email ke **pemesan** (konfirmasi booking)
- Kirim email ke **pemandu** (notifikasi assignment)
- Kirim lagi saat admin update status (Confirmed/Cancelled) — *pola sama* dgn `homestays/views.py` L288-311

### 4.8 Dashboard Admin — Statistik & Recent Bookings

**`dashboard/views.py`** — tambahkan:
```python
from guide.models import Guide, PackageBooking

total_guides = Guide.objects.filter(is_available=True).count()
total_package_bookings = PackageBooking.objects.count()
package_bookings_pending = PackageBooking.objects.filter(status='pending').count()
recent_package_bookings = PackageBooking.objects.select_related(
    'tour_package', 'guide'
).order_by('-created_at')[:5]
```

**`dashboard/home.html`** — tambahkan:
- Stat card: Total Pemandu Wisata
- Status card: Pemesanan Paket Wisata (Pending/Confirmed/Total)
- Recent bookings: Pemesanan Paket Terbaru

### 4.9 Sidebar Admin — Link Baru

**`adminpanel/base.html`** L59-63, tambahkan setelah "Pemesanan Produk":
```html
<a href="{% url 'guide_admin:guide_list' %}" class="sidebar-link {% if active_nav == 'pemandu' %}active{% endif %}">
    <i class="fas fa-user-tie"></i>
    <span>Pemandu Wisata</span>
</a>
<a href="{% url 'guide_admin:booking_list' %}" class="sidebar-link {% if active_nav == 'pemesanan_paket' %}active{% endif %}">
    <i class="fas fa-ticket-alt"></i>
    <span>Pemesanan Paket Wisata</span>
</a>
```

---

## 5. Data Seed — Pemandu Wisata & Paket Contoh

Buat migration `guide/migrations/0002_seed_guides.py` yang otomatis memasukkan:

### 5.1 Data Pemandu Wisata (≥ 10 orang)

| # | Nama | Kategori | Bahasa | Bio |
|---|---|---|---|---|
| 1 | Andi Saputra | Lokal | Indonesia, Sunda | Pemuda Karang Taruna, ahli trekking jalur savana |
| 2 | Siti Nurhaliza | Lokal | Indonesia, Sunda | Pemudi desa yang menguasai sejarah budaya lokal |
| 3 | Rizky Pratama | Internasional | Indonesia, English | Lulusan pariwisata, berpengalaman guide turis asing |
| 4 | Dewi Lestari | Internasional | Indonesia, English, Japanese | Mantan guide di Bali, fasih 3 bahasa |
| 5 | Budi Santoso | Lokal | Indonesia, Sunda | Petani lokal yang juga pemandu wisata agro |
| 6 | Maya Anggraini | Internasional | Indonesia, English, French | Lulusan sastra Prancis, guide budaya |
| 7 | Fajar Nugroho | Lokal | Indonesia | Pemuda desa penjelajah alam, ahli camping |
| 8 | Rahma Putri | Lokal | Indonesia, Sunda | Pengrajin tenun yang juga memandu wisata budaya |
| 9 | Dimas Arya | Internasional | Indonesia, English, Mandarin | Background hospitality management |
| 10 | Lina Marlina | Lokal | Indonesia, Sunda | Ibu rumah tangga yang aktif di wisata kuliner desa |
| 11 | Taufik Hidayat | Internasional | Indonesia, English, Korean | Pemuda desa yang belajar bahasa Korea secara otodidak |
| 12 | Nisa Aulia | Lokal | Indonesia | Pemudi karang taruna, spesialis wisata air terjun |

### 5.2 Data Paket Wisata Contoh

> *Paket dikaitkan ke destinasi yang sudah ada di database. Jika belum ada destinasi, paket tetap dibuat dan akan otomatis tampil saat destinasi di-assign.*

| # | Nama Paket | Harga Lokal | Harga Internasional | Durasi |
|---|---|---|---|---|
| 1 | Paket Sunrise Bukit Savana | Rp 150.000 | Rp 350.000 | 4 Jam |
| 2 | Paket Air Terjun & Trekking | Rp 200.000 | Rp 450.000 | 6 Jam |
| 3 | Paket Budaya & Kerajinan Desa | Rp 100.000 | Rp 250.000 | 3 Jam |
| 4 | Paket Full Day Adventure | Rp 350.000 | Rp 750.000 | Full Day |

---

## 6. URL Routing

### 6.1 Public URLs (`guide/urls.py`, `app_name='guide'`)

| Path | View | Name |
|---|---|---|
| `<slug:dest_slug>/` | `tour_package_list` | `package_list` |
| `<slug:dest_slug>/<slug:pkg_slug>/book/` | `package_booking_create` | `booking_create` |
| `booking-success/<int:pk>/` | `booking_success` | `booking_success` |

### 6.2 Admin URLs (`guide/admin_urls.py`, `app_name='guide_admin'`)

| Path | View | Name |
|---|---|---|
| `guides/` | `admin_guide_list` | `guide_list` |
| `guides/create/` | `admin_guide_create` | `guide_create` |
| `guides/<int:pk>/edit/` | `admin_guide_edit` | `guide_edit` |
| `guides/<int:pk>/delete/` | `admin_guide_delete` | `guide_delete` |
| `packages/` | `admin_package_list` | `package_list` |
| `packages/create/` | `admin_package_create` | `package_create` |
| `packages/<int:pk>/edit/` | `admin_package_edit` | `package_edit` |
| `packages/<int:pk>/delete/` | `admin_package_delete` | `package_delete` |
| `bookings/` | `admin_booking_list` | `booking_list` |
| `bookings/<int:pk>/status/` | `admin_booking_update_status` | `booking_update` |

### 6.3 Root URL (`DTPL/urls.py`) — Tambahan

```python
path('admin/guide/', include('guide.admin_urls')),
path('paket-wisata/', include('guide.urls')),
```

---

## 7. Acceptance Criteria Checklist

- [ ] Menyediakan date picker pemilihan tanggal, jam kegiatan paket wisata, dan menonaktifkan (disable) pilihan tanggal masa lalu.
- [ ] Menampilkan pilihan paket wisata lengkap dengan foto, nama, deskripsi, informasi pemandu wisata, dan itinerary.
- [ ] Menyediakan tombol pilihan kategori wisatawan antara "Lokal" atau "Mancanegara".
- [ ] Memfilter database pemandu agar hanya menampilkan yang berstatus Available pada tanggal terpilih.
- [ ] Mewajibkan alokasi pemandu dengan kemampuan bahasa asing jika kategori "Mancanegara" dipilih.
- [ ] Menampilkan profil pemandu pada halaman ringkasan pesanan.
- [ ] Tersedia informasi harga paket wisata dan call to action ke pemesanan paket wisata.
- [ ] Tersedia fitur CRUD di dashboard admin untuk update, edit, dan delete informasi pemandu wisata.
- [ ] Tersedia di dashboard admin informasi jika ada pemesanan paket wisata.
- [ ] Konfirmasi pemesanan dikirimkan kepada pemesan dan pemandu wisata via email atau WhatsApp.
- [ ] ≥ 10 pemandu wisata tersedia di database via data seed (data migration).
- [ ] Seluruh fungsi dapat langsung dilihat tanpa input manual berkat data seed.

---

## 8. Catatan Teknis Penting

1. **Pola Auth Admin**: Semua admin views harus cek `request.session.get('is_admin_logged_in')` — *pola sama* dgn `homestays/views.py`, `products/views.py`, `destinations/views.py`.
2. **Flatpickr**: Sudah tersedia via CDN di project (`homestay_detail.html`). Pakai konfigurasi sama: `minDate: "today"`, `dateFormat: "Y-m-d"`.
3. **Email via Brevo API**: *Pola sama* dgn `homestays/views.py` L16-57 (bukan `django.core.mail`). Perlu `requests` library (sudah di `requirements.txt`).
4. **Image upload**: Pakai `ImageField` + `upload_to` + `MEDIA_ROOT`/`MEDIA_URL` yang sudah dikonfigurasi (`settings.py` L173-174). `Pillow` sudah ada di `requirements.txt`.
5. **Template extends**: Admin pages extends `adminpanel/base.html`. Public pages extends `base.html`.
6. **Tidak perlu tambah dependency baru** — semua library yang dibutuhkan sudah ada.
