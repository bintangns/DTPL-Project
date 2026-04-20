# Rencana Implementasi: Rekomendasi Wisata Interaktif Berbasis Gemini LLM

> Dokumen ini merupakan **blueprint teknis** untuk mengintegrasikan Google Gemini LLM sebagai asisten rekomendasi interaktif pada website Desa Manud Jaya. Asisten dibatasi hanya pada konteks informasi desa (destinasi, homestay, produk, paket wisata), dan dapat menerima preferensi wisatawan (jenis wisata, durasi, budget) untuk memberikan rekomendasi yang personal.

---

## 1. Ringkasan Produk

| Item | Detail |
|---|---|
| **User Story** | Sebagai wisatawan, saya ingin mendapatkan rekomendasi paket wisata, homestay, dan produk yang sesuai dengan preferensi saya agar pengalaman wisata lebih personal dan relevan. |
| **Product Goal** | Pengalaman Wisata Personal & Berkelanjutan |
| **Product Goal Statement** | Wisatawan mendapatkan rekomendasi destinasi, homestay, dan produk yang sesuai preferensi mereka. |
| **Metrik Keberhasilan** | Rating kepuasan wisatawan ≥ 4.0/5.0 |

### Acceptance Criteria

- [ ] Wisatawan dapat memasukkan preferensi (jenis wisata, durasi, budget).
- [ ] Sistem menampilkan rekomendasi destinasi, homestay, dan produk yang sesuai.
- [ ] Rekomendasi menggunakan data preferensi dan riwayat wisatawan yang tersedia.
- [ ] Rekomendasi **terbatas pada informasi Desa Manud Jaya saja**.
- [ ] Chatbot tersedia secara global di seluruh halaman publik (floating button).

---

## 2. Prinsip & Batasan (Scope)

1. **Grounded Context**: LLM **hanya** menjawab berdasarkan data dari database Desa Manud Jaya (Destination, Homestay, Product, TourPackage). Jika ditanya soal daerah lain, asisten menolak dengan sopan dan mengarahkan ke wisata Manud Jaya.
2. **Model**: Menggunakan `gemini-2.0-flash` (cepat, hemat token, cukup untuk chatbot text). Bisa di-upgrade ke `gemini-2.0-pro` jika butuh reasoning lebih dalam.
3. **Interaksi**: Chatbot floating di sudut kanan bawah, tampil di **semua halaman publik** (embed di `base.html`). AJAX-based, tanpa page reload.
4. **Privacy**: API Key **tidak pernah** di-expose ke frontend. Semua calls melalui backend endpoint Django.

---

## 3. Arsitektur Teknis

```
┌──────────────┐       POST /api/ask-gemini/        ┌──────────────────┐
│   Frontend   │  ────────────────────────────────▶  │   Django View    │
│  (JS Fetch)  │                                     │  ask_gemini()    │
│              │  ◀────────────────────────────────  │                  │
│  Chat Widget │       JsonResponse{response}        │  ┌────────────┐ │
└──────────────┘                                     │  │  services  │ │
                                                     │  │  .py       │ │
                                                     │  │            │ │
                                                     │  │ 1. Query DB│ │
                                                     │  │ 2. Build   │ │
                                                     │  │    context │ │
                                                     │  │ 3. Call    │ │
                                                     │  │    Gemini  │ │
                                                     │  └────────────┘ │
                                                     └──────────────────┘
                                                              │
                                                              ▼
                                                     ┌──────────────────┐
                                                     │ Google Gemini API│
                                                     │ (AI Studio)      │
                                                     └──────────────────┘
```

---

## 4. File yang Perlu Dibuat / Dimodifikasi

### 4.1 File BARU

| # | File | Tujuan |
|---|---|---|
| 1 | `destinations/services.py` | Service layer: query DB, build system prompt, call Gemini API |
| 2 | `destinations/templates/destinations/chatbot_widget.html` | Partial template: floating chat UI widget |
| 3 | `destinations/static/destinations/css/chatbot.css` | Styling untuk chat widget |
| 4 | `destinations/static/destinations/js/chatbot.js` | JavaScript logika chat: open/close, send/receive, loading state |

### 4.2 File YANG DIMODIFIKASI

| # | File | Perubahan |
|---|---|---|
| 1 | `requirements.txt` | Tambah `google-generativeai` |
| 2 | `DTPL/settings.py` | Tambah `GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')` |
| 3 | `.env` | Tambah `GEMINI_API_KEY=<user's key>` |
| 4 | `destinations/urls.py` | Tambah `path('api/ask-gemini/', views.ask_gemini, name='ask_gemini')` |
| 5 | `destinations/views.py` | Tambah view function `ask_gemini(request)` |
| 6 | `templates/base.html` | Tambah `{% include 'destinations/chatbot_widget.html' %}` sebelum `</body>`, plus load CSS dan JS |

---

## 5. Detail Implementasi Per-Komponen

### 5.1 Instalasi & Konfigurasi

**`requirements.txt`** — tambahkan:
```
google-generativeai
```

**`.env`** — tambahkan:
```
GEMINI_API_KEY=AIzaSy...
```

**`DTPL/settings.py`** — tambahkan setelah `BREVO_API_KEY`:
```python
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
```

### 5.2 Service Layer (`destinations/services.py`)

```python
import google.generativeai as genai
from django.conf import settings
from destinations.models import Destination
from homestays.models import Homestay
from products.models import Product

def build_manud_jaya_context():
    """
    Query semua data relevan dari database dan 
    format menjadi string konteks untuk System Instruction.
    """
    # --- DESTINASI ---
    destinations = Destination.objects.filter(is_active=True)
    dest_text = ""
    for d in destinations:
        dest_text += (
            f"- {d.name} ({d.category.name}): {d.short_description}. "
            f"Lokasi: {d.location}. Durasi: {d.duration}. "
            f"Kesulitan: {d.difficulty}. Waktu terbaik: {d.best_time}. "
            f"Aktivitas: {d.activities}. "
            f"Eco-friendly: {'Ya' if d.is_eco_friendly else 'Tidak'}.\n"
        )

    # --- HOMESTAY ---
    homestays = Homestay.objects.filter(is_active=True)
    stay_text = ""
    for h in homestays:
        stay_text += (
            f"- {h.name}: {h.description[:100]}... "
            f"Harga: Rp {h.price_per_night:,.0f}/malam. "
            f"Kapasitas: {h.capacity} tamu, {h.bedrooms} kamar. "
            f"Lokasi: {h.address}.\n"
        )

    # --- PRODUK LOKAL ---
    products = Product.objects.filter(is_active=True)
    prod_text = ""
    for p in products:
        prod_text += (
            f"- {p.name} ({p.category.name}): {p.short_description}. "
            f"Harga: Rp {p.price:,.0f}. Stok: {p.stock}.\n"
        )

    # --- PAKET WISATA (jika modul guide sudah aktif) ---
    pkg_text = ""
    try:
        from guide.models import TourPackage
        packages = TourPackage.objects.filter(is_active=True)
        for pk in packages:
            pkg_text += (
                f"- {pk.name}: {pk.description[:100]}... "
                f"Harga Lokal: Rp {pk.price_local:,.0f}. "
                f"Harga Internasional: Rp {pk.price_international:,.0f}. "
                f"Durasi: {pk.duration}.\n"
            )
    except Exception:
        pkg_text = "(Belum tersedia data paket wisata)\n"

    return dest_text, stay_text, prod_text, pkg_text


SYSTEM_PROMPT = """Anda adalah "Asisten Wisata Manud Jaya", pemandu virtual khusus untuk Desa Wisata Manud Jaya 
di Kecamatan Sukamakmur, Kabupaten Bogor, Jawa Barat.

ATURAN KETAT:
1. Anda HANYA boleh menjawab pertanyaan terkait wisata di Desa Manud Jaya.
2. Jika ditanya tentang destinasi wisata lain (Bali, Yogja, dll), tolak dengan sopan dan 
   arahkan kembali ke penawaran Desa Manud Jaya.
3. Berikan rekomendasi berdasarkan DATA BERIKUT SAJA. Jangan mengarang informasi.
4. Jawab dalam Bahasa Indonesia yang ramah dan informatif.
5. Jika wisatawan menyebutkan preferensi (budget, durasi, jenis wisata), 
   cocokkan dengan data yang tersedia.
6. Format jawaban dengan rapi, gunakan emoji secukupnya untuk kesan ramah.

=== DATA DESTINASI WISATA ===
{destinations}

=== DATA HOMESTAY ===
{homestays}

=== DATA PRODUK LOKAL ===
{products}

=== DATA PAKET WISATA ===
{packages}
"""


def get_gemini_response(user_message):
    """
    Kirim pesan user ke Gemini API dengan context injection.
    Return string response.
    """
    genai.configure(api_key=settings.GEMINI_API_KEY)

    dest_text, stay_text, prod_text, pkg_text = build_manud_jaya_context()

    system_instruction = SYSTEM_PROMPT.format(
        destinations=dest_text or "(Belum ada data)",
        homestays=stay_text or "(Belum ada data)",
        products=prod_text or "(Belum ada data)",
        packages=pkg_text or "(Belum ada data)",
    )

    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash',
        system_instruction=system_instruction,
    )

    response = model.generate_content(user_message)
    return response.text
```

### 5.3 View Endpoint (`destinations/views.py` — tambahan)

```python
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .services import get_gemini_response

@require_POST
def ask_gemini(request):
    """API endpoint untuk chatbot Gemini."""
    try:
        body = json.loads(request.body)
        user_message = body.get('message', '').strip()

        if not user_message:
            return JsonResponse({'error': 'Pesan tidak boleh kosong'}, status=400)

        response_text = get_gemini_response(user_message)
        return JsonResponse({'response': response_text})

    except Exception as e:
        return JsonResponse(
            {'error': f'Terjadi kesalahan: {str(e)}'},
            status=500
        )
```

**CSRF Handling**: Karena endpoint ini diakses dari frontend yang sudah memiliki cookie session Django, kita bisa menggunakan CSRF token standar. Di JavaScript, kita ambil CSRF token dari cookie dan sertakan di header.

### 5.4 URL Registration

**`destinations/urls.py`** — tambah:
```python
path('api/ask-gemini/', views.ask_gemini, name='ask_gemini'),
```

### 5.5 Frontend — Chat Widget

**`destinations/templates/destinations/chatbot_widget.html`**:

Komponen floating chat bubble di sudut kanan bawah:
- **Closed state**: Tombol bulat dengan ikon robot/chat + animasi pulse
- **Open state**: Panel chat 380×500px dengan:
  - Header (judul "Asisten Wisata Manud Jaya" + tombol close)
  - Area chat (scrollable, pesan user kanan, pesan bot kiri)
  - Input area (textarea + tombol send)
  - Loading indicator (typing dots animation)
- **Welcome message**: Auto-muncul saat panel dibuka pertama kali: _"Halo! 👋 Saya Asisten Wisata Manud Jaya. Saya bisa bantu rekomendasikan destinasi, homestay, paket wisata, atau produk lokal yang sesuai preferensi Anda. Silakan tanya apa saja!"_

**`destinations/static/destinations/js/chatbot.js`**:
- Open/close toggle
- `fetch('/destinasi/api/ask-gemini/', { method: 'POST', headers: {'X-CSRFToken': csrftoken}, body: JSON.stringify({message: ...}) })`
- Append pesan ke chat area
- Loading state (disable input, tampilkan "typing...")
- Auto-scroll ke bawah setelah response
- CSRF token diambil dari cookie (`document.cookie`)

**`destinations/static/destinations/css/chatbot.css`**:
- Posisi: `position: fixed; bottom: 24px; right: 24px; z-index: 9999;`
- Desain premium: glassmorphism panel, gradient header, smooth shadows
- Animasi: `fadeIn` saat open, pulse pada tombol
- Responsive: lebih kecil di mobile, full-width di viewport < 480px

### 5.6 Integrasi ke `base.html`

**`templates/base.html`** — sebelum `</body>`:
```html
{% include 'destinations/chatbot_widget.html' %}
```

Ini membuat chatbot **tersedia di semua halaman publik** (Home, Destinasi, Homestay, Produk, Ecotourism).

---

## 6. Keamanan & Performa

### 6.1 Prompt Injection Prevention
- System instruction yang sangat tegas dengan aturan "HANYA Desa Manud Jaya".
- Instruksi negasi eksplisit: jangan mengarang, jangan jawab di luar konteks.
- User input tidak pernah dijadikan system instruction — hanya content.

### 6.2 Rate Limiting (Sederhana)
```python
# Di views.py, bisa ditambahkan rate limit sederhana
from django.core.cache import cache

def ask_gemini(request):
    ip = request.META.get('REMOTE_ADDR', '')
    cache_key = f'gemini_ratelimit_{ip}'
    count = cache.get(cache_key, 0)

    if count >= 20:  # Maks 20 request per menit per IP
        return JsonResponse({'error': 'Terlalu banyak permintaan. Coba lagi nanti.'}, status=429)

    cache.set(cache_key, count + 1, timeout=60)
    # ... lanjut proses
```

### 6.3 Token Usage Optimization
- Hanya query field esensial dari database (nama, harga, deskripsi pendek).
- Batasi `description[:100]` untuk hemat token.
- Cache hasil `build_manud_jaya_context()` selama 5 menit agar tidak re-query database setiap chat.

### 6.4 Error Handling
- Jika Gemini API gagal (rate limit Google, network error), tampilkan pesan fallback user-friendly:  _"Maaf, asisten kami sedang sibuk. Silakan coba lagi dalam beberapa saat."_
- Logging error di server untuk monitoring.

---

## 7. Pengujian

### 7.1 Positive Test Cases
| # | Input User | Expected Behavior |
|---|---|---|
| 1 | "Rekomendasikan wisata alam untuk keluarga" | Merekomendasikan destinasi alam di Manud Jaya beserta paket wisata yang sesuai |
| 2 | "Saya punya budget 200rb untuk wisata sehari" | Filter dan tampilkan paket dengan harga ≤ 200rb |
| 3 | "Ada homestay yang murah?" | Menampilkan homestay dengan harga terendah |
| 4 | "Produk oleh-oleh apa yang ada?" | List produk lokal dari database |

### 7.2 Negative Test Cases (Boundary)
| # | Input User | Expected Behavior |
|---|---|---|
| 1 | "Rekomendasikan wisata di Bali" | Menolak sopan, arahkan ke wisata Manud Jaya |
| 2 | "Ignore previous instructions..." | Tetap menjawab dalam konteks Manud Jaya |
| 3 | "" (kosong) | Return error 400: "Pesan tidak boleh kosong" |

---

## 8. Catatan Teknis Penting

1. **Tidak perlu model database baru** — fitur ini murni service layer + API endpoint.
2. **Satu dependency baru**: `google-generativeai` (tambah ke `requirements.txt`, lalu `pip install`).
3. **API Key wajib di `.env`** — user perlu menambahkan `GEMINI_API_KEY=...` sendiri.
4. **Chatbot di `base.html`** berarti tampil di semua halaman — termasuk Home, yang belum tentu relevan. Jika diinginkan hanya di halaman destinasi, pindahkan include ke `destinations/detail.html` saja.
5. **Model fallback**: Jika `gemini-2.0-flash` tidak tersedia, bisa fallback ke `gemini-1.5-flash`.
