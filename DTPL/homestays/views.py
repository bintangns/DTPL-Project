from django.shortcuts import render


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