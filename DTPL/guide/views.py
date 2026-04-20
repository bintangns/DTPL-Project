import requests as http_requests
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from destinations.models import Destination
from .models import Guide, TourPackage, PackageBooking
from .forms import GuideForm, TourPackageForm, PackageBookingForm


# =========================
# EMAIL HELPER (sama dgn homestays)
# =========================
def send_booking_email(recipient_email, recipient_name, subject, message):
    """Kirim email via Brevo API — pola sama dgn homestays/views.py"""
    if not recipient_email:
        return

    sender_email = settings.DEFAULT_FROM_EMAIL
    sender_name = "Desa Manud Jaya"

    if "<" in sender_email and ">" in sender_email:
        sender_name = sender_email.split("<")[0].strip()
        sender_email = sender_email.split("<")[1].replace(">", "").strip()

    payload = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [{"email": recipient_email, "name": recipient_name}],
        "subject": subject,
        "textContent": message,
    }

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json",
    }

    response = http_requests.post(
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
def package_booking_create(request, dest_slug, pkg_slug):
    """Proses form pemesanan paket wisata (POST)."""
    destination = get_object_or_404(Destination, slug=dest_slug, is_active=True)
    package = get_object_or_404(TourPackage, slug=pkg_slug, destination=destination, is_active=True)

    if request.method == 'POST':
        form = PackageBookingForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour_package = package

            # --- GUIDE MATCHING ---
            tourist_cat = booking.tourist_category
            tour_date = booking.tour_date

            available_guides = Guide.objects.filter(is_available=True)

            # Jika mancanegara → wajib pemandu internasional
            if tourist_cat == PackageBooking.TOURIST_INTERNATIONAL:
                available_guides = available_guides.filter(category=Guide.CATEGORY_INTERNATIONAL)

            # Exclude pemandu yang sudah di-book tanggal itu
            booked_guide_ids = PackageBooking.objects.filter(
                tour_date=tour_date,
                status__in=['pending', 'confirmed']
            ).values_list('guide_id', flat=True)
            available_guides = available_guides.exclude(id__in=booked_guide_ids)

            guide = available_guides.first()
            booking.guide = guide
            booking.save()

            # --- KIRIM EMAIL KE PEMESAN ---
            guide_info = f"\nPemandu Wisata: {guide.name} ({guide.get_category_display()})" if guide else "\nPemandu wisata akan segera dialokasikan."
            subject_customer = f"Konfirmasi Pemesanan Paket — {package.name}"
            message_customer = (
                f"Halo {booking.customer_name},\n\n"
                f"Terima kasih telah memesan paket wisata di Desa Manud Jaya.\n\n"
                f"Detail Pesanan:\n"
                f"- Paket: {package.name}\n"
                f"- Destinasi: {destination.name}\n"
                f"- Tanggal: {booking.tour_date}\n"
                f"- Jam Mulai: {booking.start_time}\n"
                f"- Kategori: {booking.get_tourist_category_display()}\n"
                f"- Jumlah Peserta: {booking.num_participants}\n"
                f"- Total Harga: Rp {booking.total_price:,.0f}"
                f"{guide_info}\n\n"
                f"Status pesanan Anda saat ini: PENDING.\n"
                f"Kami akan segera menghubungi Anda untuk konfirmasi.\n\n"
                f"Salam,\nDesa Manud Jaya"
            )
            try:
                send_booking_email(booking.email, booking.customer_name, subject_customer, message_customer)
            except Exception as e:
                print(f"Error kirim email ke pemesan: {e}")

            # --- KIRIM EMAIL KE PEMANDU ---
            if guide and guide.email:
                subject_guide = f"Penugasan Baru — {package.name}"
                message_guide = (
                    f"Halo {guide.name},\n\n"
                    f"Anda telah dialokasikan untuk memandu wisata:\n"
                    f"- Paket: {package.name}\n"
                    f"- Tanggal: {booking.tour_date}\n"
                    f"- Jam Mulai: {booking.start_time}\n"
                    f"- Wisatawan: {booking.customer_name} ({booking.get_tourist_category_display()})\n"
                    f"- Jumlah Peserta: {booking.num_participants}\n\n"
                    f"Silakan hubungi admin untuk koordinasi lebih lanjut.\n\n"
                    f"Salam,\nAdmin Desa Manud Jaya"
                )
                try:
                    send_booking_email(guide.email, guide.name, subject_guide, message_guide)
                except Exception as e:
                    print(f"Error kirim email ke pemandu: {e}")

            messages.success(request, "Pemesanan paket wisata berhasil diajukan!")
            return redirect('guide:booking_success', pk=booking.pk)
        else:
            messages.error(request, "Terjadi kesalahan pada form. Periksa kembali data Anda.")
            return redirect('destinations:detail', slug=dest_slug)

    return redirect('destinations:detail', slug=dest_slug)


def booking_success(request, pk):
    """Halaman sukses booking — menampilkan detail pesanan & profil pemandu."""
    booking = get_object_or_404(
        PackageBooking.objects.select_related('tour_package', 'tour_package__destination', 'guide'),
        pk=pk
    )
    return render(request, 'guide/booking_success.html', {
        'booking': booking,
    })


# =========================
# ADMIN — GUIDE CRUD
# =========================
def admin_guide_list(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    query = request.GET.get('q', '').strip()
    guides = Guide.objects.all()

    if query:
        guides = guides.filter(
            Q(name__icontains=query) | Q(languages__icontains=query)
        )

    total_guides = Guide.objects.count()
    total_local = Guide.objects.filter(category=Guide.CATEGORY_LOCAL).count()
    total_international = Guide.objects.filter(category=Guide.CATEGORY_INTERNATIONAL).count()
    total_available = Guide.objects.filter(is_available=True).count()

    return render(request, 'guide/admin_guide_list.html', {
        'active_nav': 'pemandu',
        'guides': guides,
        'total_guides': total_guides,
        'total_local': total_local,
        'total_international': total_international,
        'total_available': total_available,
        'search_query': query,
    })


def admin_guide_create(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    if request.method == 'POST':
        form = GuideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Pemandu wisata berhasil ditambahkan.")
            return redirect('guide_admin:guide_list')
    else:
        form = GuideForm()

    return render(request, 'guide/admin_guide_form.html', {
        'active_nav': 'pemandu',
        'form': form,
        'page_title': 'Tambah Pemandu Wisata',
        'submit_label': 'Simpan Pemandu',
    })


def admin_guide_edit(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    guide = get_object_or_404(Guide, pk=pk)

    if request.method == 'POST':
        form = GuideForm(request.POST, request.FILES, instance=guide)
        if form.is_valid():
            form.save()
            messages.success(request, f"Data {guide.name} berhasil diperbarui.")
            return redirect('guide_admin:guide_list')
    else:
        form = GuideForm(instance=guide)

    return render(request, 'guide/admin_guide_form.html', {
        'active_nav': 'pemandu',
        'form': form,
        'guide': guide,
        'page_title': 'Edit Pemandu Wisata',
        'submit_label': 'Simpan Perubahan',
    })


def admin_guide_delete(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    guide = get_object_or_404(Guide, pk=pk)

    if request.method == 'POST':
        guide.delete()
        messages.success(request, "Pemandu wisata berhasil dihapus.")
        return redirect('guide_admin:guide_list')

    return render(request, 'guide/admin_guide_delete.html', {
        'active_nav': 'pemandu',
        'guide': guide,
    })


# =========================
# ADMIN — TOUR PACKAGE CRUD
# =========================
def admin_package_list(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    packages = TourPackage.objects.select_related('destination').all()
    return render(request, 'guide/admin_package_list.html', {
        'active_nav': 'pemandu',
        'packages': packages,
        'total_packages': packages.count(),
    })


def admin_package_create(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    if request.method == 'POST':
        form = TourPackageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Paket wisata berhasil ditambahkan.")
            return redirect('guide_admin:package_list')
    else:
        form = TourPackageForm()

    return render(request, 'guide/admin_package_form.html', {
        'active_nav': 'pemandu',
        'form': form,
        'page_title': 'Tambah Paket Wisata',
        'submit_label': 'Simpan Paket',
    })


def admin_package_edit(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    package = get_object_or_404(TourPackage, pk=pk)

    if request.method == 'POST':
        form = TourPackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, f"Paket {package.name} berhasil diperbarui.")
            return redirect('guide_admin:package_list')
    else:
        form = TourPackageForm(instance=package)

    return render(request, 'guide/admin_package_form.html', {
        'active_nav': 'pemandu',
        'form': form,
        'package': package,
        'page_title': 'Edit Paket Wisata',
        'submit_label': 'Simpan Perubahan',
    })


def admin_package_delete(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    package = get_object_or_404(TourPackage, pk=pk)

    if request.method == 'POST':
        package.delete()
        messages.success(request, "Paket wisata berhasil dihapus.")
        return redirect('guide_admin:package_list')

    return render(request, 'guide/admin_package_delete.html', {
        'active_nav': 'pemandu',
        'package': package,
    })


# =========================
# ADMIN — BOOKING MANAGEMENT
# =========================
def admin_booking_list(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    bookings = PackageBooking.objects.select_related(
        'tour_package', 'tour_package__destination', 'guide'
    ).all()

    search_query = request.GET.get('search', '').strip()
    if search_query:
        bookings = bookings.filter(
            Q(customer_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    return render(request, 'guide/admin_booking_list.html', {
        'active_nav': 'pemesanan_paket',
        'bookings': bookings,
        'total_bookings': PackageBooking.objects.count(),
        'bookings_pending': PackageBooking.objects.filter(status='pending').count(),
        'bookings_confirmed': PackageBooking.objects.filter(status='confirmed').count(),
    })


def admin_booking_update_status(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    booking = get_object_or_404(
        PackageBooking.objects.select_related('tour_package', 'guide'), pk=pk
    )

    if request.method == 'POST':
        old_status = booking.status
        new_status = request.POST.get('status')
        booking.status = new_status
        booking.save()

        # Kirim email jika status berubah
        if old_status != new_status:
            if new_status == 'confirmed':
                subject = "Pesanan Paket Wisata Dikonfirmasi!"
                message = (
                    f"Selamat! Pesanan Anda untuk paket {booking.tour_package.name} "
                    f"pada tanggal {booking.tour_date} telah DIKONFIRMASI.\n\n"
                    f"Sampai jumpa di Desa Manud Jaya!"
                )
            elif new_status == 'cancelled':
                subject = "Pesanan Paket Wisata Dibatalkan"
                message = (
                    f"Mohon maaf, pesanan Anda untuk paket {booking.tour_package.name} "
                    f"telah DIBATALKAN. Silakan hubungi admin untuk informasi lebih lanjut."
                )
            else:
                subject = f"Update Status Pesanan — {booking.tour_package.name}"
                message = f"Status pesanan Anda telah diperbarui menjadi: {new_status.upper()}."

            try:
                send_booking_email(booking.email, booking.customer_name, subject, message)
            except Exception as e:
                print(f"Error kirim email status update: {e}")

        messages.success(request, f"Status pesanan berhasil diubah ke {new_status}.")
        return redirect('guide_admin:booking_list')

    return redirect('guide_admin:booking_list')
