"""Data migration: seed 6 destinations from hardcoded data."""

from django.db import migrations


def seed_destinations(apps, schema_editor):
    DestinationCategory = apps.get_model('destinations', 'DestinationCategory')
    Destination = apps.get_model('destinations', 'Destination')

    # Create category
    eco_cat, _ = DestinationCategory.objects.get_or_create(
        name='Alam',
        defaults={'slug': 'alam'},
    )

    destinations_data = [
        {
            'name': 'Air Terjun Kembar',
            'slug': 'air-terjun-kembar',
            'location': 'Dusun Kembar, 4 km dari pusat desa',
            'short_description': (
                'Air terjun kembar dengan ketinggian 30 meter, dikelilingi hutan '
                'tropis yang asri. Tempat ideal untuk berenang dan bersantai '
                'sambil menikmati kesejukan alam.'
            ),
            'description': (
                'Air Terjun Kembar merupakan salah satu keajaiban alam Desa Manud '
                'Jaya yang paling fotogenik. Dua aliran air terjun berdampingan '
                'dengan ketinggian masing-masing 30 meter jatuh ke kolam alami '
                'yang luas dan berair jernih kebiruan. Dikelilingi oleh hutan '
                'tropis yang lebat, kawasan ini menjadi habitat bagi berbagai '
                'jenis kupu-kupu, burung, dan flora endemik seperti anggrek hutan '
                'dan paku-pakuan raksasa. Suara gemericik air berpadu dengan '
                'kicauan burung menciptakan suasana damai dan menyegarkan. '
                'Pengunjung dapat berenang di kolam alami yang aman (kedalaman '
                'bervariasi 1\u20134 meter), bermain air di tepian, atau sekadar '
                'duduk di bebatuan halus sambil menikmati semprotan air yang '
                'sejuk. Air terjun ini juga dipercaya memiliki nilai sakral oleh '
                'masyarakat setempat, sehingga pengunjung diimbau untuk menjaga '
                'perilaku dan tidak membuang sampah sembarangan. Area ini dikelola '
                'dengan prinsip ecotourism, termasuk pembatasan jumlah pengunjung '
                'harian (maksimal 100 orang/hari) dan larangan penggunaan '
                'sabun/shampoo di sungai untuk menjaga kualitas air serta '
                'ekosistem perairan.\n\n'
                'Cara Akses: Dari pusat desa, perjalanan menuju Dusun Kembar sejauh 4 km '
                'dapat ditempuh dengan kendaraan roda dua atau roda empat '
                '(20 menit). Jalan beraspal baik hingga area parkir resmi. '
                'Setelah tiba di area parkir, pengunjung akan melanjutkan '
                'perjalanan dengan berjalan kaki menyusuri jalur setapak sejauh '
                '800 meter yang telah dilengkapi dengan papan petunjuk, jembatan '
                'kayu, dan tangga batu. Jalur ini relatif mudah dan dapat '
                'dilalui oleh semua usia, dengan pemandangan hutan sekunder, '
                'kebun warga, dan aliran sungai kecil di sepanjang perjalanan.'
            ),
            'image_url': 'https://images.unsplash.com/photo-1494472155656-f34e81b17ddc?w=800',
            'duration': '2\u20133 jam',
            'difficulty': 'Mudah',
            'best_time': 'Mei \u2013 Oktober (musim kemarau)',
            'features': (
                'Area parkir kendaraan luas dan aman, '
                'Toilet ramah lingkungan dan ruang ganti, '
                'Gazebo untuk bersantai dan piknik, '
                'Warung makan tradisional, '
                'Penyewaan pelampung dan tikar, '
                'Spot foto dengan platform kayu'
            ),
            'activities': 'Berenang, Fotografi, Trekking ringan',
            'is_eco_friendly': True,
        },
        {
            'name': 'Bukit Savana Lestari',
            'slug': 'bukit-savana-lestari',
            'location': 'Dusun Savana, 7 km dari pusat desa',
            'short_description': (
                'Padang rumput perbukitan dengan pemandangan luas dan spot '
                'matahari terbenam yang memukau. Cocok untuk trekking ringan, '
                'piknik, dan fotografi lanskap.'
            ),
            'description': (
                'Bukit Savana Lestari menawarkan hamparan padang rumput alami '
                'di ketinggian 400 mdpl dengan panorama perbukitan hijau yang '
                'membentang sejauh mata memandang. Kawasan ini menjadi habitat '
                'bagi berbagai jenis burung dan kupu\u2011kupu, serta beberapa '
                'satwa liar seperti kijang dan lutung. Saat senja, langit '
                'berubah warna menjadi jingga keemasan, menciptakan momen '
                'fotografi yang tak terlupakan. Area ini dikelola dengan '
                'pembatasan jumlah pengunjung dan jalur trekking khusus untuk '
                'mencegah erosi tanah.\n\n'
                'Cara Akses: Dari pusat desa, pengunjung dapat menggunakan kendaraan roda '
                'dua atau roda empat menuju basecamp Savana (jarak 5 km), '
                'kemudian dilanjutkan dengan trekking ringan sejauh 2 km '
                'melalui jalur setapak yang telah dilengkapi papan interpretasi '
                'alam. Tersedia pula jasa pemandu lokal yang siap menemani '
                'perjalanan.'
            ),
            'image_url': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800',
            'duration': '3\u20134 jam',
            'difficulty': 'Mudah hingga sedang',
            'best_time': 'Mei \u2013 September (musim kemarau)',
            'features': (
                'Area parkir kendaraan di basecamp, '
                'Pos istirahat dengan tempat duduk kayu, '
                'Shelter untuk berteduh, '
                'Toilet ramah lingkungan, '
                'Papan informasi jalur trekking, '
                'Spot foto dengan platform kayu'
            ),
            'activities': 'Trekking, Fotografi, Piknik',
            'is_eco_friendly': True,
        },
        {
            'name': 'Danau Cermin',
            'slug': 'danau-cermin',
            'location': 'Dusun Danau, 2 km dari pusat desa',
            'short_description': (
                'Danau alami dengan air jernih seperti cermin, dikelilingi '
                'pepohonan rindang. Aktivitas: memancing, berperahu, atau '
                'sekadar bersantai di tepi danau.'
            ),
            'description': (
                'Danau Cermin terbentuk dari mata air alami yang muncul di '
                'cekungan perbukitan, menciptakan danau seluas 3 hektar dengan '
                'kedalaman hingga 8 meter. Airnya sangat jernih sehingga '
                'memantulkan bayangan pepohonan dan langit di sekitarnya\u2014'
                'itulah asal nama Danau Cermin. Ekosistem danau dihuni oleh '
                'berbagai jenis ikan air tawar seperti nila, mujair, dan gabus, '
                'serta bunga teratai yang mekar di musim tertentu. Pengunjung '
                'dapat memancing (dengan izin), menyewa perahu dayung, atau '
                'sekadar duduk santai di tepi danau sambil menikmati udara sejuk.\n\n'
                'Cara Akses: Dari pusat desa, perjalanan menuju Dusun Danau sejauh 2 km '
                'dapat ditempuh dengan kendaraan roda dua atau berjalan kaki '
                'menyusuri pematang sawah yang indah. Jalur setapak telah '
                'diperbaiki dengan paving block dan dilengkapi penerangan '
                'tenaga surya.'
            ),
            'image_url': 'https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=800',
            'duration': '2\u20133 jam',
            'difficulty': 'Sangat mudah',
            'best_time': 'Pagi atau sore hari untuk cuaca cerah',
            'features': (
                'Area parkir luas, '
                'Penyewaan perahu dayung, '
                'Penyewaan alat pancing, '
                'Gazebo dan bangku taman, '
                'Kafe apung sederhana, '
                'Toilet dan mushola'
            ),
            'activities': 'Memancing, Berperahu, Bersantai',
            'is_eco_friendly': True,
        },
        {
            'name': 'Goa Karst Cemara',
            'slug': 'goa-karst-cemara',
            'location': 'Dusun Karst, 5 km dari pusat desa',
            'short_description': (
                'Goa alam dengan stalaktit dan stalakmit yang menakjubkan, '
                'serta sungai bawah tanah. Eksplorasi goa ditemani pemandu '
                'lokal yang menjelaskan proses geologi dan ekosistem gua.'
            ),
            'description': (
                'Goa Karst Cemara merupakan formasi batuan kapur alami yang '
                'terbentuk jutaan tahun lalu dengan panjang lorong sekitar '
                '500 meter. Di dalamnya terdapat ornamen goa yang masih aktif '
                'terbentuk, seperti stalaktit, stalakmit, pilar, dan flowstone. '
                'Aliran sungai bawah tanah yang jernih mengalir di sepanjang '
                'lorong goa, menjadi habitat bagi ikan buta dan kelelawar. '
                'Eksplorasi goa dilakukan dengan peralatan standar dan ditemani '
                'pemandu berpengalaman yang akan menjelaskan proses geologi '
                'serta mitos lokal yang berkembang.\n\n'
                'Cara Akses: Dari pusat desa, perjalanan dilanjutkan ke Dusun Karst sejauh '
                '5 km dengan kendaraan pribadi atau ojek desa. Dari titik '
                'pertemuan, pengunjung akan berjalan kaki sekitar 500 meter '
                'menuju mulut goa. Peralatan seperti helm, senter, dan sepatu '
                'anti\u2011slip dapat disewa di posko pemandu.'
            ),
            'image_url': 'https://images.unsplash.com/photo-1504699439244-ac7c242d4c17?w=800',
            'duration': '2\u20133 jam',
            'difficulty': 'Sedang',
            'best_time': 'Sepanjang tahun (hindari musim hujan lebat)',
            'features': (
                'Posko pemandu goa, '
                'Penyewaan peralatan eksplorasi, '
                'Tempat penitipan barang, '
                'Toilet dan ruang ganti, '
                'Warung makan tradisional, '
                'Area istirahat dengan gazebo'
            ),
            'activities': 'Eksplorasi goa, Fotografi, Edukasi geologi',
            'is_eco_friendly': True,
        },
        {
            'name': 'Hutan Mangrove Bahari',
            'slug': 'hutan-mangrove-bahari',
            'location': 'Dusun Bahari, 3 km dari pusat desa',
            'short_description': (
                'Kawasan hutan mangrove yang menjadi habitat berbagai burung, '
                'kepiting, dan biota laut. Nikmati trekking di jembatan kayu '
                'sambil belajar tentang peran mangrove.'
            ),
            'description': (
                'Hutan Mangrove Bahari membentang seluas 15 hektar di sepanjang '
                'pesisir selatan desa. Ekosistem ini menjadi rumah bagi berbagai '
                'jenis burung migran seperti bangau putih dan raja udang, serta '
                'biota laut seperti kepiting bakau, ikan belodok, dan '
                'kerang\u2011kerangan. Pengunjung dapat menjelajahi kawasan ini '
                'melalui jembatan kayu sepanjang 1,2 km yang dilengkapi menara '
                'pengamatan burung. Di beberapa titik, tersedia papan informasi '
                'tentang jenis\u2011jenis mangrove, siklus hidup biota laut, '
                'serta peran penting mangrove dalam mencegah abrasi dan intrusi '
                'air laut.\n\n'
                'Cara Akses: Dari pusat desa, pengunjung dapat menuju Dermaga Bahari '
                '(jarak 3 km) dengan kendaraan pribadi atau transportasi desa. '
                'Dari dermaga, perjalanan dilanjutkan dengan perahu dayung milik '
                'warga menuju kawasan mangrove (sekitar 15 menit).'
            ),
            'image_url': 'https://images.unsplash.com/photo-1569974498991-d3c12a504f95?w=800',
            'duration': '1\u20132 jam',
            'difficulty': 'Mudah',
            'best_time': 'Pagi hari (06.00\u201309.00) untuk melihat burung',
            'features': (
                'Dermaga perahu, '
                'Penyewaan perahu dayung, '
                'Jembatan kayu interpretasi, '
                'Menara pengamatan burung, '
                'Kios suvenir kerajinan mangrove, '
                'Warung kopi dengan pemandangan laut'
            ),
            'activities': 'Trekking, Pengamatan burung, Edukasi mangrove',
            'is_eco_friendly': True,
        },
        {
            'name': 'Puncak Gunung Api Purba',
            'slug': 'puncak-gunung-api-purba',
            'location': 'Dusun Gunung, 8 km dari pusat desa',
            'short_description': (
                'Puncak tertinggi di kawasan ini dengan kawah purba dan '
                'pemandangan 360 derajat. Spot favorit untuk menyaksikan '
                'matahari terbit dari atas awan.'
            ),
            'description': (
                'Puncak Gunung Api Purba merupakan sisa kaldera gunung berapi '
                'yang aktif ribuan tahun lalu, kini menjadi bukit dengan '
                'ketinggian 800 mdpl. Dari puncaknya, pengunjung dapat menikmati '
                'panorama 360 derajat yang meliputi hamparan hutan tropis, '
                'perbukitan kapur, dan garis pantai selatan. Saat matahari '
                'terbit, kabut tipis menyelimuti lembah, menciptakan pemandangan '
                'lautan awan yang spektakuler. Kawasan ini juga memiliki situs '
                'geologi berupa batuan basal dan andesit yang unik, serta kawah '
                'kecil yang kini menjadi danau musiman.\n\n'
                'Cara Akses: Perjalanan dimulai dari basecamp Gunung Api di Dusun Gunung '
                '(8 km dari pusat desa). Trekking menuju puncak memakan waktu '
                'sekitar 2\u20133 jam dengan jalur menanjak namun telah '
                'dilengkapi tangga batu dan papan petunjuk. Pendakian dianjurkan '
                'dimulai pukul 03.00 dini hari untuk tiba tepat waktu '
                'menyaksikan matahari terbit.'
            ),
            'image_url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800',
            'duration': '4\u20135 jam (pulang\u2011pergi)',
            'difficulty': 'Menantang',
            'best_time': 'Mei \u2013 September (musim kemarau)',
            'features': (
                'Basecamp pendakian, '
                'Pemandu lokal profesional, '
                'Pos peristirahatan setiap 500 meter, '
                'Tempat berkemah di area puncak, '
                'Toilet sederhana di basecamp, '
                'Kantin dengan minuman hangat'
            ),
            'activities': 'Pendakian, Fotografi, Kemping',
            'is_eco_friendly': True,
        },
    ]

    for data in destinations_data:
        Destination.objects.get_or_create(
            slug=data['slug'],
            defaults={
                'name': data['name'],
                'category': eco_cat,
                'location': data['location'],
                'short_description': data['short_description'],
                'description': data['description'],
                'image_url': data['image_url'],
                'duration': data['duration'],
                'difficulty': data['difficulty'],
                'best_time': data['best_time'],
                'features': data['features'],
                'activities': data['activities'],
                'is_eco_friendly': data['is_eco_friendly'],
            },
        )


def remove_destinations(apps, schema_editor):
    Destination = apps.get_model('destinations', 'Destination')
    Destination.objects.filter(slug__in=[
        'air-terjun-kembar',
        'bukit-savana-lestari',
        'danau-cermin',
        'goa-karst-cemara',
        'hutan-mangrove-bahari',
        'puncak-gunung-api-purba',
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_destinations, remove_destinations),
    ]
