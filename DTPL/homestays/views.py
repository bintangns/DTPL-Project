import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Homestay, HomestayBooking
from .forms import HomestayForm, PublicBookingForm
from reviews.forms import ReviewForm
from reviews.services import get_review_summary_for_instance
# =========================
# EMAIL HELPER
# =========================
import requests
from django.conf import settings

def send_order_status_email(order, subject, message):
    if not order.email:
        return

    sender_email = settings.DEFAULT_FROM_EMAIL
    sender_name = "Desa Manud Jaya"

    # Kalau format DEFAULT_FROM_EMAIL = "DTPL UI <email@domain.com>"
    if "<" in sender_email and ">" in sender_email:
        sender_name = sender_email.split("<")[0].strip()
        sender_email = sender_email.split("<")[1].replace(">", "").strip()

    payload = {
        "sender": {
            "name": sender_name,
            "email": sender_email,
        },
        "to": [
            {
                "email": order.email,
                "name": order.customer_name,
            }
        ],
        "subject": subject,
        "textContent": message,
    }

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json",
    }

    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        json=payload,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()
    return response.json()

# =========================
# PUBLIC VIEWS
# =========================

def homestay_list(request):
    """Menampilkan daftar homestay dengan fitur filter harga dan kapasitas"""
    homestays = Homestay.objects.all().order_by('-created_at')

    # Logika Filter
    price_query = request.GET.get('price')
    capacity_query = request.GET.get('capacity')

    if price_query:
        homestays = homestays.filter(price_per_night__lte=price_query)

    if capacity_query:
        homestays = homestays.filter(capacity__gte=capacity_query)

    # Menambahkan status ketersediaan secara realtime untuk badge di HTML
    today = timezone.now().date()
    for h in homestays:
        h.is_currently_booked = HomestayBooking.objects.filter(
            homestay=h,
            status='confirmed',
            check_in__lte=today,
            check_out__gte=today
        ).exists()

    context = {
        'homestays': homestays,
        'active_nav': 'homestay',
    }
    return render(request, "homestay_list.html", context)


def homestay_detail(request, slug):
    homestay = get_object_or_404(Homestay, slug=slug)
    form = PublicBookingForm()

    booked_ranges = HomestayBooking.objects.filter(
        homestay=homestay,
        status='confirmed',
        check_out__gte=timezone.now().date()
    ).values('check_in', 'check_out')

    booked_dates_json = json.dumps([
        {'from': b['check_in'].isoformat(), 'to': b['check_out'].isoformat()}
        for b in booked_ranges
    ])

    return render(request, "homestays/homestay_detail.html", {
        "homestay": homestay,
        "form": form,
        "booked_dates_json": booked_dates_json,
        "review_form": ReviewForm(),
        "review_summary": get_review_summary_for_instance(homestay),
        "review_type": "homestay",
        "object_slug": homestay.slug,
        "object_name": homestay.name,
    })


def homestay_booking_create(request, slug):
    homestay = get_object_or_404(Homestay, slug=slug)

    if request.method == 'POST':
        form = PublicBookingForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.homestay = homestay
            
            # Validasi Overlap (Tanggal bentrok)
            overlap = HomestayBooking.objects.filter(
                homestay=homestay, 
                status='confirmed'
            ).filter(
                Q(check_in__lt=booking.check_out, check_out__gt=booking.check_in)
            ).exists()

            if overlap:
                messages.error(request, "Maaf, tanggal tersebut sudah dipesan orang lain.")
                return redirect('homestays:detail', slug=slug)
            
            booking.save() # Simpan ke database (Status default: pending)
            subject = f"Konfirmasi Pemesanan - {homestay.name}"
            message = (
                f"Halo {booking.customer_name},\n\n"
                f"Terima kasih telah melakukan pemesanan di {homestay.name}.\n"
                f"Detail Pesanan:\n"
                f"- Check-in: {booking.check_in}\n"
                f"- Check-out: {booking.check_out}\n"
                f"- Total Harga: Rp {booking.total_price:,.0f}\n\n"
                f"Status pesanan Anda saat ini adalah PENDING. Kami akan segera memverifikasi "
                f"bukti pembayaran Anda dan mengirimkan email konfirmasi lanjutan.\n\n"
                f"Salam,\nDesa Manud Jaya"
            )

            try:
                send_order_status_email(booking, subject, message)
            except Exception as e:
                # Kita tidak ingin user gagal booking hanya karena email gagal kirim
                # Jadi kita cukup print log-nya saja
                print(f"Error kirim email: {e}")
            
            messages.success(request, "Booking berhasil diajukan! Silakan tunggu konfirmasi admin.")
            return redirect('homestays:list')
        else:
            messages.error(request, "Terjadi kesalahan pada form. Periksa kembali data Anda.")
            return redirect('homestays:detail', slug=slug)

    return redirect('homestays:detail', slug=slug)

# =========================
# ADMIN CRUD: HOMESTAY
# =========================

def admin_homestay_list(request):
    """Dashboard daftar homestay untuk Admin"""
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    homestays = Homestay.objects.all().order_by('-id')
    return render(request, 'homestays/admin_homestay_list.html', {
        'homestays': homestays,
        'active_nav': 'homestay',
        'total_homestays': homestays.count()
    })

def admin_homestay_create(request):
    if request.method == 'POST':
        # Ambil semua input fasilitas[]
        fac_list = request.POST.getlist('facilities[]')
        # Bersihkan dari string kosong
        fac_list = [f.strip() for f in fac_list if f.strip()]
        
        # Simpan manual karena kita bypass Django Form untuk field ini
        homestay = Homestay.objects.create(
            name=request.POST.get('name'),
            owner=request.POST.get('owner'),
            description=request.POST.get('description'),
            price_per_night=request.POST.get('price_per_night'),
            capacity=request.POST.get('capacity'), # Simpan sebagai teks
            bedrooms=request.POST.get('bedrooms'),
            bathrooms=request.POST.get('bathrooms'),
            image_url=request.POST.get('image_url'),
            address=request.POST.get('address'),
            facilities=json.dumps(fac_list) # Ubah list jadi string JSON
        )
        return redirect('homestays_admin:list')
    return render(request, 'homestays/admin_form.html', {'title': 'Tambah Homestay'})

def admin_homestay_update(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    homestay = get_object_or_404(Homestay, pk=pk)

    if request.method == 'POST':
        homestay.name = request.POST.get('name')
        homestay.slug = request.POST.get('slug')
        homestay.owner = request.POST.get('owner')
        homestay.price_per_night = request.POST.get('price_per_night')
        homestay.image_url = request.POST.get('image_url')
        homestay.capacity = request.POST.get('capacity')
        homestay.bedrooms = request.POST.get('bedrooms')
        homestay.bathrooms = request.POST.get('bathrooms')
        homestay.address = request.POST.get('address')
        homestay.description = request.POST.get('description')

        fac_list = request.POST.getlist('facilities[]')
        fac_list = [f.strip() for f in fac_list if f.strip()] 
        homestay.facilities = json.dumps(fac_list)

        # 5. Simpan ke Database
        homestay.save()

        messages.success(request, f"Data {homestay.name} berhasil diperbarui.")
        return redirect('homestays_admin:list')

    return render(request, 'homestays/admin_form.html', {
        'homestay': homestay, 
        'title': 'Edit Homestay'
    })

def admin_homestay_delete(request, pk):
    """Hapus Homestay"""
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')
        
    homestay = get_object_or_404(Homestay, pk=pk)
    if request.method == 'POST':
        homestay.delete()
        messages.success(request, "Homestay telah dihapus.")
    return redirect('homestays_admin:list')


# =========================
# ADMIN: BOOKING MANAGEMENT
# =========================

def admin_homestay_booking_list(request):
    """Daftar seluruh pesanan masuk untuk Admin"""
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    bookings = HomestayBooking.objects.all().order_by('-created_at')
    search_query = request.GET.get('search')
    if search_query:
        bookings = bookings.filter(
            Q(customer_name__icontains=search_query) | 
            Q(email__icontains=search_query)
        )

    # 3. Logika Filter Status
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    # 4. Data untuk Statistik Dashboard
    context = {
        'bookings': bookings,
        'total_bookings': HomestayBooking.objects.count(),
        'bookings_pending': HomestayBooking.objects.filter(status='pending').count(),
        'bookings_confirmed': HomestayBooking.objects.filter(status='confirmed').count(),
        'title': 'Pemesanan Homestay'
    }
    
    return render(request, 'homestays/admin_booking_list.html', context)

def admin_booking_update_status(request, pk):
    """Update status booking (Pending, Confirmed, Cancelled)"""
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')
        
    order = get_object_or_404(HomestayBooking, pk=pk)
    if request.method == 'POST':
        old_status = order.status
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()

        # --- LOGIKA KIRIM EMAIL BERDASARKAN STATUS BARU ---
        if old_status != new_status:
            if new_status == 'confirmed':
                subject = "Pembayaran Diterima - Pesanan Dikonfirmasi!"
                message = f"Selamat! Pesanan Anda di {order.homestay.name} telah DIKONFIRMASI. Sampai jumpa di Desa Manud Jaya!"
            elif new_status == 'cancelled':
                subject = "Pesanan Dibatalkan"
                message = f"Mohon maaf, pesanan Anda di {order.homestay.name} telah DIBATALKAN. Silakan hubungi admin untuk informasi lebih lanjut."
            
            # Eksekusi kirim
            send_order_status_email(order, subject, message)

        return redirect('homestays_admin:booking_list')