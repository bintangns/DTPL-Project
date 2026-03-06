from django.shortcuts import render, get_object_or_404

def product_list(request):
    category = request.GET.get('category')

    products = [
        {
            'name': 'Kopi Arabika Manud Jaya',
            'slug': 'kopi-arabika-manud-jaya',
            'category': 'kopi',
            'category_display': 'Kopi',
            'price': 50000,
            'stock': 20,
            'short_description': 'Kopi arabika khas desa dengan aroma yang harum.',
            'image': 'https://via.placeholder.com/300x200?text=Kopi+Arabika',
        },
        {
            'name': 'Kopi Robusta Tradisional',
            'slug': 'kopi-robusta-tradisional',
            'category': 'kopi',
            'category_display': 'Kopi',
            'price': 45000,
            'stock': 15,
            'short_description': 'Kopi robusta dengan cita rasa kuat dan khas.',
            'image': 'https://via.placeholder.com/300x200?text=Kopi+Robusta',
        },
        {
            'name': 'Cokelat Batang Premium',
            'slug': 'cokelat-batang-premium',
            'category': 'cokelat',
            'category_display': 'Cokelat',
            'price': 35000,
            'stock': 12,
            'short_description': 'Cokelat batang premium dari kakao lokal pilihan.',
            'image': 'https://via.placeholder.com/300x200?text=Cokelat+Batang',
        },
        {
            'name': 'Bubuk Kakao Organik',
            'slug': 'bubuk-kakao-organik',
            'category': 'cokelat',
            'category_display': 'Cokelat',
            'price': 40000,
            'stock': 8,
            'short_description': 'Bubuk kakao organik untuk minuman dan baking.',
            'image': 'https://via.placeholder.com/300x200?text=Bubuk+Kakao',
        },
    ]

    if category in ['kopi', 'cokelat']:
        products = [p for p in products if p['category'] == category]

    context = {
        'products': products,
        'selected_category': category,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    products = [
        {
            'name': 'Kopi Arabika Manud Jaya',
            'slug': 'kopi-arabika-manud-jaya',
            'category': 'kopi',
            'category_display': 'Kopi',
            'price': 50000,
            'stock': 20,
            'short_description': 'Kopi arabika khas desa dengan aroma yang harum.',
            'description': 'Kopi arabika berkualitas tinggi yang diolah langsung oleh masyarakat desa.',
            'image': 'https://via.placeholder.com/500x300?text=Kopi+Arabika',
        },
        {
            'name': 'Kopi Robusta Tradisional',
            'slug': 'kopi-robusta-tradisional',
            'category': 'kopi',
            'category_display': 'Kopi',
            'price': 45000,
            'stock': 15,
            'short_description': 'Kopi robusta dengan cita rasa kuat dan khas.',
            'description': 'Kopi robusta tradisional dengan rasa pekat dan cocok untuk penikmat kopi asli.',
            'image': 'https://via.placeholder.com/500x300?text=Kopi+Robusta',
        },
        {
            'name': 'Cokelat Batang Premium',
            'slug': 'cokelat-batang-premium',
            'category': 'cokelat',
            'category_display': 'Cokelat',
            'price': 35000,
            'stock': 12,
            'short_description': 'Cokelat batang premium dari kakao lokal pilihan.',
            'description': 'Produk cokelat lokal premium dengan rasa autentik dan tekstur lembut.',
            'image': 'https://via.placeholder.com/500x300?text=Cokelat+Batang',
        },
        {
            'name': 'Bubuk Kakao Organik',
            'slug': 'bubuk-kakao-organik',
            'category': 'cokelat',
            'category_display': 'Cokelat',
            'price': 40000,
            'stock': 8,
            'short_description': 'Bubuk kakao organik untuk minuman dan baking.',
            'description': 'Bubuk kakao organik hasil olahan masyarakat desa, cocok untuk minuman sehat.',
            'image': 'https://via.placeholder.com/500x300?text=Bubuk+Kakao',
        },
    ]

    product = next((p for p in products if p['slug'] == slug), None)

    return render(request, 'products/product_detail.html', {'product': product})