from django.shortcuts import render
from django.http import Http404


# All destination data from the plan files — static data, no database needed.
DESTINATIONS = [
    {
        'slug': 'air-terjun-kembar',
        'name': 'Air Terjun Kembar',
        'tagline': (
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
            'ekosistem perairan.'
        ),
        'access': (
            'Dari pusat desa, perjalanan menuju Dusun Kembar sejauh 4 km '
            'dapat ditempuh dengan kendaraan roda dua atau roda empat '
            '(20 menit). Jalan beraspal baik hingga area parkir resmi. '
            'Setelah tiba di area parkir, pengunjung akan melanjutkan '
            'perjalanan dengan berjalan kaki menyusuri jalur setapak sejauh '
            '800 meter yang telah dilengkapi dengan papan petunjuk, jembatan '
            'kayu, dan tangga batu. Jalur ini relatif mudah dan dapat '
            'dilalui oleh semua usia, dengan pemandangan hutan sekunder, '
            'kebun warga, dan aliran sungai kecil di sepanjang perjalanan.'
        ),
        'facilities': [
            'Area parkir kendaraan luas dan aman',
            'Toilet ramah lingkungan dan ruang ganti',
            'Gazebo untuk bersantai dan piknik',
            'Warung makan tradisional',
            'Penyewaan pelampung dan tikar',
            'Spot foto dengan platform kayu',
        ],
        'location': 'Dusun Kembar, 4 km dari pusat desa',
        'duration': '2\u20133 jam',
        'best_time': 'Mei \u2013 Oktober (musim kemarau)',
        'difficulty': 'Mudah',
        'image': 'destinations/images/air-terjun-kembar.jpg',
        'category': 'Ecotourism',
    },
    {
        'slug': 'bukit-savana-lestari',
        'name': 'Bukit Savana Lestari',
        'tagline': (
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
            'mencegah erosi tanah.'
        ),
        'access': (
            'Dari pusat desa, pengunjung dapat menggunakan kendaraan roda '
            'dua atau roda empat menuju basecamp Savana (jarak 5 km), '
            'kemudian dilanjutkan dengan trekking ringan sejauh 2 km '
            'melalui jalur setapak yang telah dilengkapi papan interpretasi '
            'alam. Tersedia pula jasa pemandu lokal yang siap menemani '
            'perjalanan.'
        ),
        'facilities': [
            'Area parkir kendaraan di basecamp',
            'Pos istirahat dengan tempat duduk kayu',
            'Shelter untuk berteduh',
            'Toilet ramah lingkungan',
            'Papan informasi jalur trekking',
            'Spot foto dengan platform kayu',
        ],
        'location': 'Dusun Savana, 7 km dari pusat desa',
        'duration': '3\u20134 jam',
        'best_time': 'Mei \u2013 September (musim kemarau)',
        'difficulty': 'Mudah hingga sedang',
        'image': 'destinations/images/bukit-savana-lestari.jpg',
        'category': 'Ecotourism',
    },
    {
        'slug': 'danau-cermin',
        'name': 'Danau Cermin',
        'tagline': (
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
            'sekadar duduk santai di tepi danau sambil menikmati udara sejuk.'
        ),
        'access': (
            'Dari pusat desa, perjalanan menuju Dusun Danau sejauh 2 km '
            'dapat ditempuh dengan kendaraan roda dua atau berjalan kaki '
            'menyusuri pematang sawah yang indah. Jalur setapak telah '
            'diperbaiki dengan paving block dan dilengkapi penerangan '
            'tenaga surya.'
        ),
        'facilities': [
            'Area parkir luas',
            'Penyewaan perahu dayung',
            'Penyewaan alat pancing',
            'Gazebo dan bangku taman',
            'Kafe apung sederhana',
            'Toilet dan mushola',
        ],
        'location': 'Dusun Danau, 2 km dari pusat desa',
        'duration': '2\u20133 jam',
        'best_time': 'Pagi atau sore hari untuk cuaca cerah',
        'difficulty': 'Sangat mudah',
        'image': 'destinations/images/danau-cermin.jpg',
        'category': 'Ecotourism',
    },
    {
        'slug': 'goa-karst-cemara',
        'name': 'Goa Karst Cemara',
        'tagline': (
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
            'serta mitos lokal yang berkembang.'
        ),
        'access': (
            'Dari pusat desa, perjalanan dilanjutkan ke Dusun Karst sejauh '
            '5 km dengan kendaraan pribadi atau ojek desa. Dari titik '
            'pertemuan, pengunjung akan berjalan kaki sekitar 500 meter '
            'menuju mulut goa. Peralatan seperti helm, senter, dan sepatu '
            'anti\u2011slip dapat disewa di posko pemandu.'
        ),
        'facilities': [
            'Posko pemandu goa',
            'Penyewaan peralatan eksplorasi',
            'Tempat penitipan barang',
            'Toilet dan ruang ganti',
            'Warung makan tradisional',
            'Area istirahat dengan gazebo',
        ],
        'location': 'Dusun Karst, 5 km dari pusat desa',
        'duration': '2\u20133 jam',
        'best_time': 'Sepanjang tahun (hindari musim hujan lebat)',
        'difficulty': 'Sedang',
        'image': 'destinations/images/goa-karst-cemara.jpg',
        'category': 'Ecotourism',
    },
    {
        'slug': 'hutan-mangrove-bahari',
        'name': 'Hutan Mangrove Bahari',
        'tagline': (
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
            'air laut.'
        ),
        'access': (
            'Dari pusat desa, pengunjung dapat menuju Dermaga Bahari '
            '(jarak 3 km) dengan kendaraan pribadi atau transportasi desa. '
            'Dari dermaga, perjalanan dilanjutkan dengan perahu dayung milik '
            'warga menuju kawasan mangrove (sekitar 15 menit).'
        ),
        'facilities': [
            'Dermaga perahu',
            'Penyewaan perahu dayung',
            'Jembatan kayu interpretasi',
            'Menara pengamatan burung',
            'Kios suvenir kerajinan mangrove',
            'Warung kopi dengan pemandangan laut',
        ],
        'location': 'Dusun Bahari, 3 km dari pusat desa',
        'duration': '1\u20132 jam',
        'best_time': 'Pagi hari (06.00\u201309.00) untuk melihat burung',
        'difficulty': 'Mudah',
        'image': 'destinations/images/hutan-mangrove-bahari.jpg',
        'category': 'Ecotourism',
    },
    {
        'slug': 'puncak-gunung-api-purba',
        'name': 'Puncak Gunung Api Purba',
        'tagline': (
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
            'kecil yang kini menjadi danau musiman.'
        ),
        'access': (
            'Perjalanan dimulai dari basecamp Gunung Api di Dusun Gunung '
            '(8 km dari pusat desa). Trekking menuju puncak memakan waktu '
            'sekitar 2\u20133 jam dengan jalur menanjak namun telah '
            'dilengkapi tangga batu dan papan petunjuk. Pendakian dianjurkan '
            'dimulai pukul 03.00 dini hari untuk tiba tepat waktu '
            'menyaksikan matahari terbit.'
        ),
        'facilities': [
            'Basecamp pendakian',
            'Pemandu lokal profesional',
            'Pos peristirahatan setiap 500 meter',
            'Tempat berkemah di area puncak',
            'Toilet sederhana di basecamp',
            'Kantin dengan minuman hangat',
        ],
        'location': 'Dusun Gunung, 8 km dari pusat desa',
        'duration': '4\u20135 jam (pulang\u2011pergi)',
        'best_time': 'Mei \u2013 September (musim kemarau)',
        'difficulty': 'Menantang',
        'image': 'destinations/images/puncak-gunung-api-purba.jpg',
        'category': 'Ecotourism',
    },
]


def destination_list(request):
    """Render the destination landing page with all destinations."""
    context = {'destinations': DESTINATIONS}
    return render(request, 'destinations/index.html', context)


def destination_detail(request, slug):
    """Render a single destination detail page by slug."""
    destination = None
    for dest in DESTINATIONS:
        if dest['slug'] == slug:
            destination = dest
            break
    if destination is None:
        raise Http404("Destinasi tidak ditemukan")
    context = {'dest': destination}
    return render(request, 'destinations/detail.html', context)
