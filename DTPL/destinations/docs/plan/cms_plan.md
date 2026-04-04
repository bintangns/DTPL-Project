# Destination CMS Section — Documentation Plan

## Objective

Menyediakan halaman CMS (Content Management System) untuk admin desa agar dapat mengelola konten destinasi wisata Desa Manud Jaya secara dinamis. Ini mencakup fitur CRUD (Create, Read, Update, Delete) destinasi, migrasi data destinasi dari hardcoded ke database, serta memperbarui halaman publik (frontend) agar menampilkan data dari database.

## User Story

**Sebagai** admin desa,  
**Saya ingin** dapat memperbarui informasi destinasi wisata  
**Agar** informasi yang ditampilkan kepada wisatawan selalu akurat.

### Sub-User Stories

| ID | User Story | Priority |
|----|-----------|----------|
| DS-01 | Sebagai admin, saya ingin melihat daftar semua destinasi wisata di halaman admin | Must |
| DS-02 | Sebagai admin, saya ingin melihat statistik ringkasan (total destinasi, wisata alam, wisata budaya, eco-friendly) | Must |
| DS-03 | Sebagai admin, saya ingin menambah destinasi baru beserta foto, deskripsi, dan informasi detail | Must |
| DS-04 | Sebagai admin, saya ingin mengedit informasi destinasi yang sudah ada (nama, deskripsi, foto, durasi, dll.) | Must |
| DS-05 | Sebagai admin, saya ingin menghapus destinasi dengan konfirmasi sebelumnya | Must |
| DS-06 | Sebagai admin, saya ingin mencari destinasi berdasarkan nama, lokasi, atau kategori | Should |
| DS-07 | Sebagai admin, saya ingin menandai destinasi sebagai ramah lingkungan (eco-friendly) | Should |
| DS-08 | Sebagai pengguna frontend, saya ingin melihat daftar destinasi dari database (bukan hardcoded) | Must |

## Activity Diagram (Referensi)

Alur CMS mengikuti activity diagram PBI-09:
1. Admin masuk ke Dashboard → membuka modul "Manajemen Destinasi"
2. Admin memilih aksi: **Tambah**, **Edit**, **Hapus**, atau **Moderasi Ulasan**
3. Untuk **Tambah**: Input data destinasi → Upload foto (opsional) → Simpan
4. Untuk **Edit**: Pilih destinasi → Ubah deskripsi dan/atau foto → Simpan
5. Untuk **Hapus**: Pilih destinasi → Konfirmasi hapus → Hapus destinasi
6. Untuk **Moderasi Ulasan**: Buka daftar ulasan → Setujui/Tolak/Sembunyikan (scope masa depan)
7. Jika tidak ada perubahan → Kembali ke dashboard

> **Catatan:** Fitur Moderasi Ulasan (poin 6) tidak termasuk dalam scope CMS ini dan akan diimplementasikan sebagai fitur terpisah di masa depan.

## Detailed Changes

### 1. Model Layer — `destinations/models.py`

Membuat model `Destination` yang mencakup semua field dari data hardcoded saat ini, plus field tambahan dari mockup form edit.

**Model `DestinationCategory`:**
| Field | Type | Keterangan |
|-------|------|------------|
| `name` | CharField(100) | Nama kategori (e.g. "Alam", "Budaya") |
| `slug` | SlugField | Auto-generated dari name |

**Model `Destination`:**
| Field | Type | Keterangan |
|-------|------|------------|
| `name` | CharField(150) | Nama destinasi * |
| `slug` | SlugField(unique) | Auto-generated dari name, bisa diedit |
| `category` | ForeignKey(DestinationCategory) | Kategori destinasi * |
| `location` | CharField(255) | Lokasi * |
| `short_description` | CharField(255) | Deskripsi singkat untuk kartu destinasi * |
| `description` | TextField | Deskripsi lengkap untuk halaman detail |
| `image_url` | URLField | URL foto dari Unsplash atau sumber lain |
| `duration` | CharField(50) | Durasi kunjungan (e.g. "2-3 jam") |
| `difficulty` | CharField(50) | Tingkat kesulitan (e.g. "Mudah", "Sedang") |
| `best_time` | CharField(100) | Waktu terbaik berkunjung |
| `features` | TextField(blank) | Fitur destinasi, pisahkan dengan koma |
| `activities` | TextField(blank) | Aktivitas yang tersedia, pisahkan dengan koma |
| `is_eco_friendly` | BooleanField | Destinasi ramah lingkungan |
| `is_active` | BooleanField(default=True) | Status aktif/non-aktif |
| `created_at` | DateTimeField(auto_now_add) | Tanggal dibuat |

> **Catatan:** Field `tagline`, `access`, dan `facilities` dari data hardcoded saat ini dikonsolidasikan. `tagline` → `short_description`, `access` → bisa dimasukkan ke `description`, `facilities` → `features` (comma-separated).

### 2. Forms — `destinations/forms.py` [NEW]

Membuat Django `ModelForm` untuk `Destination` sesuai mockup form edit:
- **Field yang ditampilkan:** name, slug (readonly/auto), category, location, short_description, description, image_url, duration, difficulty, best_time, features, activities, is_eco_friendly
- **Validasi:** name dan category required, slug auto-generated jika kosong
- **Widget:** textarea untuk description, checkbox untuk is_eco_friendly

### 3. Admin URLs — `destinations/admin_urls.py` [NEW]

Pola URL sesuai konvensi yang sama dengan `products/admin_urls.py`:

| URL Pattern | View | Name |
|-------------|------|------|
| `''` | `admin_destination_list` | `list` |
| `'create/'` | `admin_destination_create` | `create` |
| `'<int:pk>/edit/'` | `admin_destination_edit` | `edit` |
| `'<int:pk>/delete/'` | `admin_destination_delete` | `delete` |

`app_name = 'destinations_admin'`

### 4. Admin Views — `destinations/views.py`

Menambahkan 4 view function untuk CMS (mengikuti pola `products/views.py`):

#### `admin_destination_list(request)`
- Session auth check
- Query semua `Destination` dengan statistik: total destinasi, wisata alam, wisata budaya, eco-friendly
- Support pencarian (query parameter `q`) untuk filter berdasarkan nama/lokasi/kategori
- Render template `destinations/admin_dashboard.html`
- Context: `active_nav='destinasi'`, destinations, stats, search query

#### `admin_destination_create(request)`
- Session auth check
- GET: tampilkan form kosong
- POST: validasi dan simpan, redirect ke list
- Render template `destinations/admin_destination_form.html`

#### `admin_destination_edit(request, pk)`
- Session auth check
- GET: tampilkan form dengan data existing
- POST: validasi dan update, redirect ke list
- Render template `destinations/admin_destination_form.html`

#### `admin_destination_delete(request, pk)`
- Session auth check
- POST: hapus destinasi, redirect ke list
- Render template `destinations/admin_destination_delete.html` (halaman konfirmasi)

### 5. Public Views — `destinations/views.py` (Update)

Mengubah `destination_list` dan `destination_detail` agar membaca dari database:
- `destination_list`: `Destination.objects.filter(is_active=True)` replace hardcoded `DESTINATIONS` list
- `destination_detail`: `get_object_or_404(Destination, slug=slug, is_active=True)` replace manual loop
- Hapus variabel `DESTINATIONS` hardcoded

### 6. Admin Templates [NEW]

#### `destinations/templates/destinations/admin_dashboard.html`
- Extends `adminpanel/base.html`
- Layout sesuai mockup: header "Manajemen Destinasi", stat cards row (Total Destinasi, Wisata Alam, Wisata Budaya, Eco-Friendly), search bar, destination cards grid
- Setiap kartu menampilkan: gambar, badge kategori, badge eco, nama, lokasi, deskripsi singkat, durasi, tingkat kesulitan, tombol Edit (biru) dan Hapus (merah)
- Tombol "+ Tambah Destinasi" di header

#### `destinations/templates/destinations/admin_destination_form.html`
- Extends `adminpanel/base.html`
- Form modal/page sesuai mockup form edit: field 2 kolom (Nama + Slug, Kategori + Lokasi), textarea deskripsi, URL foto dengan preview gambar, field durasi + tingkat kesulitan, waktu terbaik, fitur, aktivitas, checkbox eco-friendly
- Tombol "Batal" dan "Simpan Perubahan"

#### `destinations/templates/destinations/admin_destination_delete.html`
- Extends `adminpanel/base.html`
- Halaman konfirmasi hapus dengan info destinasi yang akan dihapus

### 7. Admin CSS — `destinations/static/destinations/css/admin.css` [NEW]

CSS khusus halaman CMS Destinasi:
- Stat cards dengan warna berbeda (sesuai mockup: biru, hijau, ungu, hijau eco)
- Grid kartu destinasi responsive
- Styling form edit
- Tombol Edit (biru) dan Hapus (merah)

### 8. Sidebar Navigation Update — `adminpanel/templates/adminpanel/base.html`

Menambahkan link "Destinasi Wisata" di sidebar, di bawah "Dashboard":
```html
<a href="{% url 'destinations_admin:list' %}" class="sidebar-link {% if active_nav == 'destinasi' %}active{% endif %}">
    <i class="fas fa-map-marked-alt"></i>
    <span>Destinasi Wisata</span>
</a>
```

### 9. Project URL Registration — `DTPL/urls.py`

Menambahkan URL pattern baru:
```python
path('admin/destinations/', include('destinations.admin_urls')),
```

### 10. Data Migration — Management Command / Migration

Membuat data migration untuk memindahkan 6 destinasi hardcoded ke database:
- Membuat `DestinationCategory` "Ecotourism" (sesuai data saat ini)
- Membuat 6 record `Destination` dari data `DESTINATIONS` di `views.py`
- Mapping field: `tagline` → `short_description`, `access` dimasukkan ke akhir `description`, `facilities` → `features` (comma-separated)

### 11. Frontend Template Update

Update template publik `index.html` dan `detail.html` untuk menggunakan field model:
- `dest.tagline` → `dest.short_description`
- `dest.image` → menggunakan `dest.image_url` via `<img src="{{ dest.image_url }}">`
- `dest.facilities` loop → parse `dest.features` dari comma-separated
- Hapus penggunaan `{% static dest.image %}` karena gambar sekarang via URL

## App Structure (Setelah Perubahan)

```
destinations/
├── __init__.py
├── admin.py
├── admin_urls.py          ← [NEW]
├── apps.py
├── forms.py               ← [NEW]
├── migrations/
│   └── 000X_destination_model.py  ← [NEW]
├── models.py              ← [MODIFY] — Tambah model Destination & DestinationCategory
├── static/destinations/
│   ├── css/
│   │   ├── style.css      ← (existing, public pages)
│   │   └── admin.css      ← [NEW]
│   └── images/            ← (existing)
├── templates/destinations/
│   ├── index.html          ← [MODIFY] — Baca dari DB
│   ├── detail.html         ← [MODIFY] — Baca dari DB
│   ├── admin_dashboard.html      ← [NEW]
│   ├── admin_destination_form.html ← [NEW]
│   └── admin_destination_delete.html ← [NEW]
├── tests.py
├── urls.py
└── views.py               ← [MODIFY] — Tambah admin views, update public views
```

## Definition of Done

- [ ] Model `DestinationCategory` dan `Destination` terdefinisi di `models.py`
- [ ] Migrasi database berhasil dijalankan (`makemigrations` + `migrate`)
- [ ] Data 6 destinasi hardcoded berhasil dimigrasikan ke database
- [ ] Variabel `DESTINATIONS` hardcoded di `views.py` dihapus
- [ ] Halaman publik `/destinasi/` menampilkan destinasi dari database
- [ ] Halaman detail `/destinasi/<slug>/` menampilkan data dari database
- [ ] Sidebar admin menampilkan menu "Destinasi Wisata" dengan highlight aktif
- [ ] Halaman admin `/admin/destinations/` menampilkan daftar destinasi dengan stat cards
- [ ] Stat cards menampilkan: Total Destinasi, Wisata Alam, Wisata Budaya, Eco-Friendly
- [ ] Search bar berfungsi untuk filter berdasarkan nama/lokasi/kategori
- [ ] Kartu destinasi admin menampilkan gambar, badge, info, dan tombol Edit/Hapus
- [ ] Tombol "+ Tambah Destinasi" mengarah ke form tambah
- [ ] Form tambah/edit menampilkan semua field sesuai mockup
- [ ] Preview gambar muncul saat URL foto diisi
- [ ] Slug auto-generated dari nama destinasi
- [ ] Validasi form berjalan (field required ditandai *)
- [ ] Simpan destinasi baru berhasil dan redirect ke daftar
- [ ] Edit destinasi berhasil dan redirect ke daftar
- [ ] Hapus destinasi menampilkan halaman konfirmasi, lalu menghapus dan redirect
- [ ] Semua halaman admin membutuhkan session login
- [ ] Admin CSS terpisah di `admin.css` dan tidak mengganggu halaman publik

## Verification Plan

### Automated Tests

Menjalankan unit test Django di `destinations/tests.py`:

```bash
python manage.py test destinations -v 2
```

Test yang akan ditambahkan:
1. **Model test:** Pastikan `Destination` dan `DestinationCategory` bisa dibuat, slug auto-generated
2. **View test — public:** Pastikan `destination_list` dan `destination_detail` mengembalikan data dari DB
3. **View test — admin (tanpa login):** Pastikan redirect ke login untuk semua admin view
4. **View test — admin CRUD:** Pastikan create, edit, delete berjalan setelah login session aktif

### Manual Verification

1. **Jalankan server lokal:** `python manage.py runserver`
2. **Buka halaman publik** http://127.0.0.1:8000/destinasi/ — pastikan 6 destinasi tampil dari database
3. **Login admin** http://127.0.0.1:8000/admin/ (username: `admin`, password: `admin123`)
4. **Klik "Destinasi Wisata"** di sidebar — pastikan halaman manajemen destinasi muncul
5. **Verifikasi stat cards** — pastikan angka total destinasi, wisata alam, dll. benar
6. **Klik "+ Tambah Destinasi"** — pastikan form muncul dengan semua field
7. **Isi dan simpan** destinasi baru — pastikan muncul di daftar
8. **Klik "Edit"** pada salah satu destinasi — pastikan form terisi data existing, edit dan simpan
9. **Klik "Hapus"** — pastikan halaman konfirmasi muncul, konfirmasi hapus, pastikan destinasi hilang dari daftar
10. **Buka kembali halaman publik** — pastikan perubahan dari CMS tercermin
