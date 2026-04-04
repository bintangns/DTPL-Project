from django.shortcuts import render, redirect
from django.db.models import Sum, Count

from products.models import Product, ProductOrder
from homestays.models import Homestay


def dashboard_home(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    # --- Product stats (real DB) ---
    total_products = Product.objects.filter(is_active=True).count()

    product_orders = ProductOrder.objects.all()
    total_product_orders = product_orders.count()
    product_orders_pending = product_orders.filter(status=ProductOrder.STATUS_PENDING).count()
    product_orders_confirmed = product_orders.filter(status=ProductOrder.STATUS_CONFIRMED).count()
    product_orders_completed = product_orders.filter(
        status=ProductOrder.STATUS_COMPLETED
    ).count()

    # Revenue from confirmed + completed orders
    confirmed_statuses = [
        ProductOrder.STATUS_CONFIRMED,
        ProductOrder.STATUS_READY_PICKUP,
        ProductOrder.STATUS_SHIPPING,
        ProductOrder.STATUS_COMPLETED,
    ]
    total_revenue = product_orders.filter(
        status__in=confirmed_statuses
    ).aggregate(
        total=Sum('product__price')
    )['total'] or 0

    # Recent product orders
    recent_product_orders = ProductOrder.objects.select_related(
        'product'
    ).order_by('-created_at')[:5]

    # --- Homestay stats (hardcoded) ---
    homestays_data = [
        {
            'name': 'Rumah Kayu Tradisional Pak Budi',
            'slug': 'rumah-modern-pak-budi',
            'owner': 'Pak Budi Santoso',
            'price_per_night': 250000,
        },
        {
            'name': 'Villa Bambu Bu Sari',
            'slug': 'villa-bambu-bu-sari',
            'owner': 'Bu Sari Wulandari',
            'price_per_night': 350000,
        },
        {
            'name': 'Pondok Sawah Pak Agus',
            'slug': 'pondok-sawah-pak-agus',
            'owner': 'Pak Agus Prasetyo',
            'price_per_night': 150000,
        },
        {
            'name': 'Rumah Teras Bu Ningsih',
            'slug': 'rumah-teras-bu-ningsih',
            'owner': 'Bu Ningsih Rahayu',
            'price_per_night': 200000,
        },
        {
            'name': 'Kabin Puncak Pak Joko',
            'slug': 'kabin-puncak-pak-joko',
            'owner': 'Pak Joko Widodo',
            'price_per_night': 300000,
        },
        {
            'name': 'Lumbung Padi Tradisional Pak Hadi',
            'slug': 'lumbung-padi-pak-hadi',
            'owner': 'Pak Hadi Suprianto',
            'price_per_night': 220000,
        },
    ]
    total_homestays = len(homestays_data)

    # --- Homestay bookings (hardcoded) ---
    homestay_bookings = [
        {
            'code': 'HJ-2026-001',
            'guest_name': 'Budi Santoso',
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
            'homestay_name': 'Villa Sawah Asri',
            'check_in': '2026-03-25',
            'check_out': '2026-03-27',
            'total': 900000,
            'status': 'pending',
            'status_display': 'Pending',
        },
    ]

    homestay_bookings_pending = len([b for b in homestay_bookings if b['status'] == 'pending'])
    homestay_bookings_confirmed = len([b for b in homestay_bookings if b['status'] == 'confirmed'])
    total_homestay_bookings = len(homestay_bookings)

    # Total transactions
    total_transactions = total_product_orders + total_homestay_bookings

    # Format revenue
    total_revenue_formatted = f"Rp {total_revenue:,.0f}".replace(',', '.')

    context = {
        'active_nav': 'dashboard',
        # Stats
        'total_revenue_formatted': total_revenue_formatted,
        'total_homestays': total_homestays,
        'total_products': total_products,
        'total_transactions': total_transactions,
        'total_homestay_bookings': total_homestay_bookings,
        'total_product_orders': total_product_orders,
        # Homestay booking status
        'homestay_bookings_pending': homestay_bookings_pending,
        'homestay_bookings_confirmed': homestay_bookings_confirmed,
        'total_homestay_bookings': total_homestay_bookings,
        # Product order status
        'product_orders_pending': product_orders_pending,
        'product_orders_confirmed': product_orders_confirmed,
        'total_product_orders': total_product_orders,
        # Recent
        'recent_homestay_bookings': homestay_bookings[:5],
        'recent_product_orders': recent_product_orders,
    }
    return render(request, 'dashboard/home.html', context)
