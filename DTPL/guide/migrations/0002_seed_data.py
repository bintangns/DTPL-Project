from django.db import migrations


def seed_guides(apps, schema_editor):
    Guide = apps.get_model('guide', 'Guide')

    guides_data = [
        {
            'name': 'Andi Saputra',
            'slug': 'andi-saputra',
            'category': 'lokal',
            'languages': 'Indonesia, Sunda',
            'phone_number': '081234567801',
            'email': 'andi.saputra@manudjaya.id',
            'bio': 'Pemuda Karang Taruna yang ahli trekking jalur savana. Sudah memandu wisatawan lokal selama 3 tahun.',
            'is_available': True,
        },
        {
            'name': 'Siti Nurhaliza',
            'slug': 'siti-nurhaliza',
            'category': 'lokal',
            'languages': 'Indonesia, Sunda',
            'phone_number': '081234567802',
            'email': 'siti.nurhaliza@manudjaya.id',
            'bio': 'Pemudi desa yang menguasai sejarah budaya lokal dan tradisi masyarakat Manud Jaya.',
            'is_available': True,
        },
        {
            'name': 'Rizky Pratama',
            'slug': 'rizky-pratama',
            'category': 'internasional',
            'languages': 'Indonesia, English',
            'phone_number': '081234567803',
            'email': 'rizky.pratama@manudjaya.id',
            'bio': 'Lulusan pariwisata yang berpengalaman memandu turis asing. Fasih berbahasa Inggris.',
            'is_available': True,
        },
        {
            'name': 'Dewi Lestari',
            'slug': 'dewi-lestari',
            'category': 'internasional',
            'languages': 'Indonesia, English, Japanese',
            'phone_number': '081234567804',
            'email': 'dewi.lestari@manudjaya.id',
            'bio': 'Mantan guide di Bali dengan pengalaman 5 tahun. Fasih 3 bahasa termasuk Jepang.',
            'is_available': True,
        },
        {
            'name': 'Budi Santoso',
            'slug': 'budi-santoso',
            'category': 'lokal',
            'languages': 'Indonesia, Sunda',
            'phone_number': '081234567805',
            'email': 'budi.santoso@manudjaya.id',
            'bio': 'Petani lokal yang juga aktif sebagai pemandu wisata agro. Mengenal setiap sudut kebun desa.',
            'is_available': True,
        },
        {
            'name': 'Maya Anggraini',
            'slug': 'maya-anggraini',
            'category': 'internasional',
            'languages': 'Indonesia, English, French',
            'phone_number': '081234567806',
            'email': 'maya.anggraini@manudjaya.id',
            'bio': 'Lulusan sastra Prancis yang kini menjadi guide budaya. Spesialis tur heritage dan kerajinan.',
            'is_available': True,
        },
        {
            'name': 'Fajar Nugroho',
            'slug': 'fajar-nugroho',
            'category': 'lokal',
            'languages': 'Indonesia',
            'phone_number': '081234567807',
            'email': 'fajar.nugroho@manudjaya.id',
            'bio': 'Pemuda desa penjelajah alam yang ahli camping dan survival di hutan. Favorit wisatawan petualang.',
            'is_available': True,
        },
        {
            'name': 'Rahma Putri',
            'slug': 'rahma-putri',
            'category': 'lokal',
            'languages': 'Indonesia, Sunda',
            'phone_number': '081234567808',
            'email': 'rahma.putri@manudjaya.id',
            'bio': 'Pengrajin tenun tradisional yang juga memandu wisata budaya. Ahli dalam sejarah kain lokal.',
            'is_available': True,
        },
        {
            'name': 'Dimas Arya',
            'slug': 'dimas-arya',
            'category': 'internasional',
            'languages': 'Indonesia, English, Mandarin',
            'phone_number': '081234567809',
            'email': 'dimas.arya@manudjaya.id',
            'bio': 'Background hospitality management. Sangat ramah dan profesional melayani wisatawan dari China dan Taiwan.',
            'is_available': True,
        },
        {
            'name': 'Lina Marlina',
            'slug': 'lina-marlina',
            'category': 'lokal',
            'languages': 'Indonesia, Sunda',
            'phone_number': '081234567810',
            'email': 'lina.marlina@manudjaya.id',
            'bio': 'Ibu rumah tangga yang aktif di wisata kuliner desa. Spesialis tur kuliner dan memasak tradisional.',
            'is_available': True,
        },
        {
            'name': 'Taufik Hidayat',
            'slug': 'taufik-hidayat',
            'category': 'internasional',
            'languages': 'Indonesia, English, Korean',
            'phone_number': '081234567811',
            'email': 'taufik.hidayat@manudjaya.id',
            'bio': 'Pemuda desa yang belajar bahasa Korea secara otodidak. Populer di kalangan wisatawan Korea Selatan.',
            'is_available': True,
        },
        {
            'name': 'Nisa Aulia',
            'slug': 'nisa-aulia',
            'category': 'lokal',
            'languages': 'Indonesia',
            'phone_number': '081234567812',
            'email': 'nisa.aulia@manudjaya.id',
            'bio': 'Pemudi karang taruna spesialis wisata air terjun. Menguasai jalur-jalur tersembunyi di hutan.',
            'is_available': True,
        },
    ]

    for guide_data in guides_data:
        Guide.objects.get_or_create(slug=guide_data['slug'], defaults=guide_data)


def seed_tour_packages(apps, schema_editor):
    TourPackage = apps.get_model('guide', 'TourPackage')
    Destination = apps.get_model('destinations', 'Destination')

    # Try to get the first few destinations to link packages
    destinations = list(Destination.objects.all()[:4])

    if not destinations:
        # No destinations in DB yet, skip package seeding
        return

    packages_data = [
        {
            'name': 'Paket Sunrise Bukit Savana',
            'slug': 'paket-sunrise-bukit-savana',
            'description': 'Nikmati keindahan matahari terbit dari puncak Bukit Savana Manud Jaya. Perjalanan dimulai dini hari dengan trekking ringan, kemudian menikmati sarapan di atas bukit dengan pemandangan 360 derajat.',
            'itinerary': '04:30 - Kumpul di basecamp\n05:00 - Mulai trekking ke puncak\n05:45 - Tiba di puncak, menunggu sunrise\n06:30 - Sarapan di puncak\n07:30 - Foto & eksplorasi area\n08:30 - Turun kembali ke basecamp',
            'price_local': 150000,
            'price_international': 350000,
            'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
            'duration': '4 Jam',
            'max_participants': 15,
            'is_active': True,
        },
        {
            'name': 'Paket Air Terjun & Trekking',
            'slug': 'paket-air-terjun-trekking',
            'description': 'Petualangan trekking menyusuri hutan tropis menuju air terjun tersembunyi Manud Jaya. Cocok untuk pecinta alam dan fotografi.',
            'itinerary': '08:00 - Briefing & persiapan\n08:30 - Mulai trekking\n10:00 - Istirahat di pos pertama\n11:00 - Tiba di air terjun\n12:00 - Makan siang di alam\n13:00 - Berenang & foto\n14:00 - Perjalanan pulang',
            'price_local': 200000,
            'price_international': 450000,
            'image_url': 'https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=800',
            'duration': '6 Jam',
            'max_participants': 12,
            'is_active': True,
        },
        {
            'name': 'Paket Budaya & Kerajinan Desa',
            'slug': 'paket-budaya-kerajinan-desa',
            'description': 'Pelajari budaya dan kerajinan tradisional Desa Manud Jaya. Termasuk workshop tenun, membuat kerajinan bambu, dan demo masakan tradisional.',
            'itinerary': '09:00 - Tur keliling desa\n10:00 - Workshop tenun tradisional\n11:30 - Membuat kerajinan bambu\n12:00 - Makan siang tradisional',
            'price_local': 100000,
            'price_international': 250000,
            'image_url': 'https://images.unsplash.com/photo-1590736969955-71cc94901144?w=800',
            'duration': '3 Jam',
            'max_participants': 20,
            'is_active': True,
        },
        {
            'name': 'Paket Full Day Adventure',
            'slug': 'paket-full-day-adventure',
            'description': 'Paket petualangan seharian penuh menggabungkan trekking, air terjun, wisata budaya, dan kuliner desa. Pengalaman terlengkap di Manud Jaya.',
            'itinerary': '06:00 - Sunrise trekking\n08:00 - Sarapan kampung\n09:30 - Trekking ke air terjun\n12:00 - Makan siang tradisional\n13:30 - Workshop budaya\n15:00 - Tur kebun & agrowisata\n16:30 - Free time & oleh-oleh\n17:00 - Penutupan',
            'price_local': 350000,
            'price_international': 750000,
            'image_url': 'https://images.unsplash.com/photo-1551632811-561732d1e306?w=800',
            'duration': 'Full Day (11 Jam)',
            'max_participants': 10,
            'is_active': True,
        },
    ]

    for i, pkg_data in enumerate(packages_data):
        dest = destinations[i % len(destinations)]
        pkg_data['destination'] = dest
        TourPackage.objects.get_or_create(slug=pkg_data['slug'], defaults=pkg_data)


def reverse_seed(apps, schema_editor):
    Guide = apps.get_model('guide', 'Guide')
    TourPackage = apps.get_model('guide', 'TourPackage')
    TourPackage.objects.all().delete()
    Guide.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0001_initial'),
        ('destinations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_guides, reverse_seed),
        migrations.RunPython(seed_tour_packages, reverse_seed),
    ]
