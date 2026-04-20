from google import genai
from django.conf import settings


def build_manud_jaya_context():
    """
    Query semua data relevan dari database dan
    format menjadi string konteks untuk System Instruction Gemini.
    """
    from destinations.models import Destination
    from homestays.models import Homestay
    from products.models import Product

    # --- DESTINASI ---
    destinations = Destination.objects.filter(is_active=True).select_related('category')
    dest_text = ""
    for d in destinations:
        cat_name = d.category.name if d.category else "Umum"
        dest_text += (
            f"- {d.name} ({cat_name}): {d.short_description}. "
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
            f"- {h.name}: {h.description[:120]}... "
            f"Harga: Rp {h.price_per_night:,.0f}/malam. "
            f"Kapasitas: {h.capacity} tamu, {h.bedrooms} kamar. "
            f"Lokasi: {h.address}.\n"
        )

    # --- PRODUK LOKAL ---
    products = Product.objects.filter(is_active=True).select_related('category')
    prod_text = ""
    for p in products:
        cat_name = p.category.name if p.category else "Umum"
        prod_text += (
            f"- {p.name} ({cat_name}): {p.short_description}. "
            f"Harga: Rp {p.price:,.0f}. Stok: {p.stock}.\n"
        )

    # --- PAKET WISATA ---
    pkg_text = ""
    try:
        from guide.models import TourPackage
        packages = TourPackage.objects.filter(is_active=True).select_related('destination')
        for pk in packages:
            pkg_text += (
                f"- {pk.name} (Destinasi: {pk.destination.name}): {pk.description[:120]}... "
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
2. Jika ditanya tentang destinasi wisata lain (Bali, Yogja, Paris, dll), tolak dengan sopan dan
   arahkan kembali ke penawaran Desa Manud Jaya.
3. Berikan rekomendasi berdasarkan DATA BERIKUT SAJA. Jangan mengarang informasi yang tidak ada di data.
4. Jawab dalam Bahasa Indonesia yang ramah dan informatif.
5. Jika wisatawan menyebutkan preferensi (budget, durasi, jenis wisata),
   cocokkan dengan data yang tersedia.
6. Format jawaban dengan rapi, gunakan emoji secukupnya untuk kesan ramah.
7. Jika ditanya sesuatu yang tidak ada di data, jawab "Maaf, informasi tersebut belum tersedia di sistem kami. Silakan hubungi tim kami di 0812 2345 5678 untuk informasi lebih lanjut."

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
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    dest_text, stay_text, prod_text, pkg_text = build_manud_jaya_context()

    system_instruction = SYSTEM_PROMPT.format(
        destinations=dest_text or "(Belum ada data destinasi)",
        homestays=stay_text or "(Belum ada data homestay)",
        products=prod_text or "(Belum ada data produk)",
        packages=pkg_text or "(Belum ada data paket wisata)",
    )

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_message,
        config={
            'system_instruction': system_instruction,
        },
    )

    return response.text
