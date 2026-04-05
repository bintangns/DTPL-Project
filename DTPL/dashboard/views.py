from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from products.models import Product, ProductOrder
from homestays.models import Homestay, HomestayBooking # Pastikan import ini benar

def dashboard_home(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    # --- PRODUCT STATS (Sudah benar) ---
    total_products = Product.objects.filter(is_active=True).count()
    product_orders = ProductOrder.objects.all()
    total_product_orders = product_orders.count()
    product_orders_pending = product_orders.filter(status='pending').count()
    product_orders_confirmed = product_orders.filter(status='confirmed').count()

    # --- HOMESTAY STATS (REAL DB) ---
    # Mengambil jumlah homestay asli dari database
    total_homestays = Homestay.objects.count()

    # Mengambil data booking asli dari database
    all_homestay_bookings = HomestayBooking.objects.all()
    total_homestay_bookings = all_homestay_bookings.count()
    homestay_bookings_pending = all_homestay_bookings.filter(status='pending').count()
    homestay_bookings_confirmed = all_homestay_bookings.filter(status='confirmed').count()

    # --- REVENUE CALCULATION (PRODUCT + HOMESTAY) ---
    # Pendapatan Produk
    confirmed_product_statuses = ['confirmed', 'ready_pickup', 'shipping', 'completed']
    revenue_product = product_orders.filter(
        status__in=confirmed_product_statuses
    ).aggregate(total=Sum('product__price'))['total'] or 0

    # Pendapatan Homestay (Hanya yang Confirmed/Completed)
    revenue_homestay = all_homestay_bookings.filter(
        status__in=['confirmed', 'completed']
    ).aggregate(total=Sum('total_price'))['total'] or 0

    total_revenue = revenue_product + revenue_homestay

    # --- RECENT DATA ---
    # Ambil 5 booking homestay terbaru
    recent_homestay_bookings = HomestayBooking.objects.select_related('homestay').order_by('-created_at')[:5]
    
    # Ambil 5 order produk terbaru
    recent_product_orders = ProductOrder.objects.select_related('product').order_by('-created_at')[:5]

    # --- FORMATTING & CONTEXT ---
    total_revenue_formatted = f"Rp {total_revenue:,.0f}".replace(',', '.')

    context = {
        'active_nav': 'dashboard',
        'total_revenue_formatted': total_revenue_formatted,
        'total_homestays': total_homestays,
        'total_products': total_products,
        'total_transactions': total_product_orders + total_homestay_bookings,
        
        'homestay_bookings_pending': homestay_bookings_pending,
        'homestay_bookings_confirmed': homestay_bookings_confirmed,
        'total_homestay_bookings': total_homestay_bookings,
        
        'product_orders_pending': product_orders_pending,
        'product_orders_confirmed': product_orders_confirmed,
        'total_product_orders': total_product_orders,
        
        'recent_homestay_bookings': recent_homestay_bookings,
        'recent_product_orders': recent_product_orders,
    }
    return render(request, 'dashboard/home.html', context)