from django.shortcuts import render, redirect


def homestay_list(request):

    homestays = [
        {
            "name": "Rumah Modern Pak Budi",
            "slug": "rumah-modern-pak-budi",
            "owner": "Pak Budi Santoso",
            "description": "Rumah kayu tradisional dengan arsitektur Jawa autentik, dikelilingi kebun organik yang asri.",
            "price_per_night": 250000,
            "capacity": 4,
            "bedrooms": 2,
            "bathrooms": 1,
            "address": "Dusun Manud, 2 km dari pusat desa",
            "image_url": "https://images.unsplash.com/photo-1505691938895-1758d7feb511",
            "facilities": ["WiFi", "Parkir", "Sarapan", "Dapur"]
        },
        {
            "name": "Villa Bambu Bu Sari",
            "slug": "villa-bambu-bu-sari",
            "owner": "Bu Sari Wulandari",
            "description": "Villa bambu modern dengan konsep eco-friendly, dilengkapi taman tropis yang indah.",
            "price_per_night": 350000,
            "capacity": 6,
            "bedrooms": 3,
            "bathrooms": 2,
            "address": "Dusun Jaya, 1.5 km dari pusat desa",
            "image_url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6",
            "facilities": ["WiFi", "Parkir", "AC", "Kolam Renang"]
        },
        {
            "name": "Pondok Sawah Pak Agus",
            "slug": "pondok-sawah-pak-agus",
            "owner": "Pak Agus Prasetyo",
            "description": "Pondok sederhana dengan pemandangan sawah yang menakjubkan.",
            "price_per_night": 150000,
            "capacity": 2,
            "bedrooms": 1,
            "bathrooms": 1,
            "address": "Dusun Jaya, 1 km dari pusat desa",
            "image_url": "https://images.unsplash.com/photo-1572120360610-d971b9d7767c",
            "facilities": ["Parkir", "Sarapan"]
        },
        {
            "name": "Rumah Teras Bu Ningsih",
            "slug": "rumah-teras-bu-ningsih",
            "owner": "Bu Ningsih Rahayu",
            "description": "Rumah dengan teras luas yang menghadap taman bunga.",
            "price_per_night": 200000,
            "capacity": 3,
            "bedrooms": 1,
            "bathrooms": 1,
            "address": "Dusun Manud, 2.5 km dari pusat desa",
            "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
            "facilities": ["WiFi", "Parkir", "Dapur"]
        },
        {
            "name": "Kabin Puncak Pak Joko",
            "slug": "kabin-puncak-pak-joko",
            "owner": "Pak Joko Widodo",
            "description": "Kabin kayu di lereng bukit dengan pemandangan spektakuler. Tempat sempurna untuk menikmati alam.",
            "price_per_night": 300000,
            "capacity": 4,
            "bedrooms": 2,
            "bathrooms": 2,
            "address": "Dusun Puncak, 3.5 km dari pusat desa",
            "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750",
            "facilities": ["WiFi", "Parkir", "Perapian", "BBQ Area"]
        }
    ]

    price = request.GET.get("price")
    capacity = request.GET.get("capacity")

    if price:
        homestays = [
            h for h in homestays
            if h["price_per_night"] <= int(price)
        ]

    if capacity:
        homestays = [
            h for h in homestays
            if h["capacity"] >= int(capacity)
        ]

    context = {
        "homestays": homestays
    }

    return render(request, "homestay_list.html", context)

def homestay_detail(request, slug):
    homestays = [
        {
            "name": "Rumah Modern Pak Budi",
            "slug": "rumah-modern-pak-budi",
            "owner": "Pak Budi Santoso",
            "description": "Rumah kayu tradisional dengan arsitektur Jawa autentik, dikelilingi kebun organik yang asri.",
            "price_per_night": 250000,
            "capacity": 4,
            "bedrooms": 2,
            "bathrooms": 1,
            "address": "Dusun Manud, 2 km dari pusat desa",
            "image_url": "https://images.unsplash.com/photo-1505691938895-1758d7feb511",
            "facilities": ["WiFi", "Parkir", "Sarapan", "Dapur"]
        },
        {
            "name": "Villa Bambu Bu Sari",
            "slug": "villa-bambu-bu-sari",
            "owner": "Bu Sari Wulandari",
            "description": "Villa bambu modern dengan konsep eco-friendly, dilengkapi taman tropis yang indah.",
            "price_per_night": 350000,
            "capacity": 6,
            "bedrooms": 3,
            "bathrooms": 2,
            "address": "Dusun Jaya, 1.5 km dari pusat desa",
            "image_url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6",
            "facilities": ["WiFi", "Parkir", "AC", "Kolam Renang"]
        },
        {
            "name": "Pondok Sawah Pak Agus",
            "slug": "pondok-sawah-pak-agus",
            "owner": "Pak Agus Prasetyo",
            "description": "Pondok sederhana dengan pemandangan sawah yang menakjubkan.",
            "price_per_night": 150000,
            "capacity": 2,
            "bedrooms": 1,
            "bathrooms": 1,
            "address": "Dusun Jaya, 1 km dari pusat desa",
            "image_url": "https://images.unsplash.com/photo-1572120360610-d971b9d7767c",
            "facilities": ["Parkir", "Sarapan"]
        },
        {
            "name": "Rumah Teras Bu Ningsih",
            "slug": "rumah-teras-bu-ningsih",
            "owner": "Bu Ningsih Rahayu",
            "description": "Rumah dengan teras luas yang menghadap taman bunga.",
            "price_per_night": 200000,
            "capacity": 3,
            "bedrooms": 1,
            "bathrooms": 1,
            "address": "Dusun Manud, 2.5 km dari pusat desa",
            "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
            "facilities": ["WiFi", "Parkir", "Dapur"]
        },
        {
            "name": "Kabin Puncak Pak Joko",
            "slug": "kabin-puncak-pak-joko",
            "owner": "Pak Joko Widodo",
            "description": "Kabin kayu di lereng bukit dengan pemandangan spektakuler.",
            "price_per_night": 300000,
            "capacity": 4,
            "bedrooms": 2,
            "bathrooms": 2,
            "address": "Dusun Puncak, 3.5 km dari pusat desa",
            "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750",
            "facilities": ["WiFi", "Parkir", "Perapian", "BBQ Area"]
        }
    ]

    homestay = None
    for h in homestays:
        if h["slug"] == slug:
            homestay = h
            break

    context = {
        "homestay": homestay
    }

    return render(request, "homestay_detail.html", context)


# =========================
# ADMIN VIEWS (Hardcoded)
# =========================

ADMIN_HOMESTAYS = [
    {
        "name": "Rumah Kayu Tradisional Pak Budi",
        "owner": "Pak Budi Santoso",
        "description": "Rumah kayu tradisional dengan arsitektur Jawa autentik, dikelilingi kebun organik yang asri.",
        "price_per_night": 250000,
        "capacity": 4,
        "bedrooms": 2,
        "bathrooms": 1,
        "image_url": "https://images.unsplash.com/photo-1505691938895-1758d7feb511",
        "eco_friendly": True,
    },
    {
        "name": "Villa Bambu Bu Sari",
        "owner": "Bu Sari Wulandari",
        "description": "Villa bambu modern dengan konsep eco-friendly, dilengkapi taman tropis yang indah.",
        "price_per_night": 350000,
        "capacity": 6,
        "bedrooms": 3,
        "bathrooms": 2,
        "image_url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6",
        "eco_friendly": True,
    },
    {
        "name": "Pondok Sawah Pak Agus",
        "owner": "Pak Agus Prasetyo",
        "description": "Pondok sederhana dengan pemandangan sawah yang menakjubkan. Ideal untuk relaksasi.",
        "price_per_night": 150000,
        "capacity": 2,
        "bedrooms": 1,
        "bathrooms": 1,
        "image_url": "https://images.unsplash.com/photo-1572120360610-d971b9d7767c",
        "eco_friendly": True,
    },
    {
        "name": "Rumah Teras Bu Ningsih",
        "owner": "Bu Ningsih Rahayu",
        "description": "Rumah dengan teras luas yang menghadap ke taman bunga. Suasana hangat dan nyaman.",
        "price_per_night": 200000,
        "capacity": 3,
        "bedrooms": 1,
        "bathrooms": 1,
        "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
        "eco_friendly": False,
    },
    {
        "name": "Kabin Puncak Pak Joko",
        "owner": "Pak Joko Widodo",
        "description": "Kabin kayu di lereng bukit dengan pemandangan spektakuler. Tempat sempurna untuk menikmati alam.",
        "price_per_night": 300000,
        "capacity": 4,
        "bedrooms": 2,
        "bathrooms": 2,
        "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750",
        "eco_friendly": False,
    },
    {
        "name": "Lumbung Padi Tradisional Pak Hadi",
        "owner": "Pak Hadi Suprianto",
        "description": "Pengalaman unik menginap di lumbung padi yang telah direnovasi menjadi penginapan nyaman.",
        "price_per_night": 220000,
        "capacity": 3,
        "bedrooms": 1,
        "bathrooms": 1,
        "image_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9",
        "eco_friendly": True,
    },
]

ADMIN_HOMESTAY_BOOKINGS = [
    {
        'code': 'HJ-2026-001',
        'guest_name': 'Budi Santoso',
        'email': 'budi.santoso@email.com',
        'homestay_name': 'Rumah Bambu Hijau',
        'check_in': '2026-03-20',
        'check_out': '2026-03-22',
        'total': 400000,
        'status': 'confirmed',
        'status_display': 'Dikonfirmasi',
    },
    {
        'code': 'HJ-2026-002',
        'guest_name': 'Siti Nurhaliza',
        'email': 'siti.nurhaliza@email.com',
        'homestay_name': 'Villa Sawah Asri',
        'check_in': '2026-03-25',
        'check_out': '2026-03-27',
        'total': 900000,
        'status': 'pending',
        'status_display': 'Pending',
    },
]


def admin_homestay_list(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    homestays = ADMIN_HOMESTAYS
    total = len(homestays)
    eco_friendly_count = len([h for h in homestays if h.get('eco_friendly')])
    total_capacity = sum(h['capacity'] for h in homestays)
    avg_price = sum(h['price_per_night'] for h in homestays) // total if total else 0

    context = {
        'active_nav': 'homestay',
        'homestays': homestays,
        'total_homestays': total,
        'eco_friendly_count': eco_friendly_count,
        'total_capacity': total_capacity,
        'avg_price': f"Rp {avg_price:,.0f}".replace(',', '.'),
    }
    return render(request, 'homestays/admin_homestay_list.html', context)


def admin_homestay_booking_list(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    bookings = ADMIN_HOMESTAY_BOOKINGS
    total = len(bookings)
    pending = len([b for b in bookings if b['status'] == 'pending'])
    confirmed = len([b for b in bookings if b['status'] == 'confirmed'])
    completed = len([b for b in bookings if b['status'] == 'completed'])

    context = {
        'active_nav': 'pemesanan_homestay',
        'bookings': bookings,
        'total_bookings': total,
        'bookings_pending': pending,
        'bookings_confirmed': confirmed,
        'bookings_completed': completed,
    }
    return render(request, 'homestays/admin_booking_list.html', context)