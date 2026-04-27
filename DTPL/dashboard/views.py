from collections import Counter
import json
from django.shortcuts import render, redirect
from django.db.models import Sum, Count, F, FloatField, ExpressionWrapper, DurationField, Avg
from products.models import Product, ProductOrder
from homestays.models import Homestay, HomestayBooking
from reviews.models import Review
from guide.models import Guide, PackageBooking
from datetime import date, timedelta
from django.http import HttpResponse
from django.db.models.functions import TruncMonth

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

    # --- GUIDE & PACKAGE STATS ---
    total_guides = Guide.objects.filter(is_available=True).count()
    all_package_bookings = PackageBooking.objects.all()
    total_package_bookings = all_package_bookings.count()
    package_bookings_pending = all_package_bookings.filter(status='pending').count()
    package_bookings_confirmed = all_package_bookings.filter(status='confirmed').count()

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

    # Pendapatan Paket Wisata
    revenue_packages = all_package_bookings.filter(
        status__in=['confirmed', 'completed']
    ).aggregate(total=Sum('total_price'))['total'] or 0

    total_revenue = revenue_product + revenue_homestay + revenue_packages

    # --- RECENT DATA ---
    # Ambil 5 booking homestay terbaru
    recent_homestay_bookings = HomestayBooking.objects.select_related('homestay').order_by('-created_at')[:5]
    
    # Ambil 5 order produk terbaru
    recent_product_orders = ProductOrder.objects.select_related('product').order_by('-created_at')[:5]

    # Ambil 5 booking paket wisata terbaru
    recent_package_bookings = PackageBooking.objects.select_related(
        'tour_package', 'guide'
    ).order_by('-created_at')[:5]

    # --- FORMATTING & CONTEXT ---
    total_revenue_formatted = f"Rp {total_revenue:,.0f}".replace(',', '.')

    context = {
        'active_nav': 'dashboard',
        'total_revenue_formatted': total_revenue_formatted,
        'total_homestays': total_homestays,
        'total_products': total_products,
        'total_transactions': total_product_orders + total_homestay_bookings + total_package_bookings,
        
        'homestay_bookings_pending': homestay_bookings_pending,
        'homestay_bookings_confirmed': homestay_bookings_confirmed,
        'total_homestay_bookings': total_homestay_bookings,
        
        'product_orders_pending': product_orders_pending,
        'product_orders_confirmed': product_orders_confirmed,
        'total_product_orders': total_product_orders,

        'total_guides': total_guides,
        'package_bookings_pending': package_bookings_pending,
        'package_bookings_confirmed': package_bookings_confirmed,
        'total_package_bookings': total_package_bookings,
        
        'recent_homestay_bookings': recent_homestay_bookings,
        'recent_product_orders': recent_product_orders,
        'recent_package_bookings': recent_package_bookings,
    }
    return render(request, 'dashboard/home.html', context)

def _parse_period(request):
    """Return (date_from, date_to, period_key, period_label) from GET params."""
    period = request.GET.get('period', 'this_month')
    today  = date.today()
 
    if period == 'this_month':
        date_from = today.replace(day=1)
        date_to   = today
        label     = today.strftime('%B %Y')
    elif period == 'last_month':
        first_this     = today.replace(day=1)
        last_month_end = first_this - timedelta(days=1)
        date_from      = last_month_end.replace(day=1)
        date_to        = last_month_end
        label          = last_month_end.strftime('%B %Y')
    elif period == 'this_year':
        date_from = today.replace(month=1, day=1)
        date_to   = today
        label     = str(today.year)
    elif period == 'last_year':
        date_from = today.replace(year=today.year - 1, month=1, day=1)
        date_to   = today.replace(year=today.year - 1, month=12, day=31)
        label     = str(today.year - 1)
    elif period == 'custom':
        try:
            date_from = date.fromisoformat(request.GET.get('date_from', ''))
            date_to   = date.fromisoformat(request.GET.get('date_to', ''))
            label     = f"{date_from.strftime('%d %b %Y')} – {date_to.strftime('%d %b %Y')}"
        except ValueError:
            date_from = today.replace(day=1)
            date_to   = today
            label     = today.strftime('%B %Y')
    else:
        date_from = today.replace(day=1)
        date_to   = today
        label     = today.strftime('%B %Y')
 
    return date_from, date_to, period, label
 
 
def _fmt_rupiah(value):
    return f"Rp {int(value):,}".replace(',', '.')
 
 
 
# ════════════════════════════════════════════════════════════════════════════
#  PBI-12 ─ ANALYTICS DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
 
def analytics_dashboard(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')
 
    date_from, date_to, period, period_label = _parse_period(request)
 
    # ── Filtered querysets (berdasarkan periode yang dipilih) ─────────────────
    homestay_qs = HomestayBooking.objects.filter(
        created_at__date__gte=date_from, created_at__date__lte=date_to)
    product_qs = ProductOrder.objects.filter(
        created_at__date__gte=date_from, created_at__date__lte=date_to)
    package_qs = PackageBooking.objects.filter(
        created_at__date__gte=date_from, created_at__date__lte=date_to)
 
    confirmed_product = ['confirmed', 'ready_pickup', 'shipping', 'completed']
    confirmed_other   = ['confirmed', 'completed']
 
    # ── KPI Utama ─────────────────────────────────────────────────────────────
    total_visitors     = homestay_qs.count() + package_qs.count()
    rev_homestay       = homestay_qs.filter(status__in=confirmed_other).aggregate(
                            t=Sum('total_price'))['t'] or 0
    rev_product        = product_qs.filter(status__in=confirmed_product).aggregate(
                            t=Sum('product__price'))['t'] or 0
    rev_package        = package_qs.filter(status__in=confirmed_other).aggregate(
                            t=Sum('total_price'))['t'] or 0
    total_revenue      = rev_homestay + rev_product + rev_package
    total_transactions = homestay_qs.count() + product_qs.count() + package_qs.count()
    avg_revenue        = total_revenue / total_transactions if total_transactions else 0
 
    # ── Breakdown cards ───────────────────────────────────────────────────────
    breakdown = [
        {
            'label': 'Homestay', 'count': homestay_qs.count(),
            'revenue': float(rev_homestay), 'revenue_fmt': _fmt_rupiah(rev_homestay),
            'icon': 'fa-bed', 'color': '#3b82f6',
        },
        {
            'label': 'Produk Lokal', 'count': product_qs.count(),
            'revenue': float(rev_product), 'revenue_fmt': _fmt_rupiah(rev_product),
            'icon': 'fa-box-open', 'color': '#f59e0b',
        },
        {
            'label': 'Paket Wisata', 'count': package_qs.count(),
            'revenue': float(rev_package), 'revenue_fmt': _fmt_rupiah(rev_package),
            'icon': 'fa-map-marked-alt', 'color': '#10b981',
        },
    ]
 
    # ── Rentang 6 bulan terakhir ──────────────────────────────────────────────
    today          = date.today()
    six_months_ago = (today.replace(day=1) - timedelta(days=150)).replace(day=1)
 
    # Daftar awal-bulan untuk 6 bulan terakhir (urut lama → baru)
    months = [
        (today.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
        for i in range(5, -1, -1)
    ]
 
    # ── Helper: revenue per bulan ─────────────────────────────────────────────
    def monthly_revenue(model, price_field, statuses):
        return {
            r['month'].date().replace(day=1): float(r['total'])
            for r in model.objects
            .filter(created_at__date__gte=six_months_ago, status__in=statuses)
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(total=Sum(price_field))
        }
 
    # ── Helper: count booking per bulan ──────────────────────────────────────
    def monthly_count(model):
        return {
            r['month'].date().replace(day=1): r['cnt']
            for r in model.objects
            .filter(created_at__date__gte=six_months_ago)
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(cnt=Count('id'))
        }
 
    # ── Data chart revenue ────────────────────────────────────────────────────
    hs_d   = monthly_revenue(HomestayBooking, 'total_price', confirmed_other)
    pkg_d  = monthly_revenue(PackageBooking,  'total_price', confirmed_other)
    prod_d = {
        r['month'].date().replace(day=1): float(r['total'])
        for r in ProductOrder.objects
        .filter(created_at__date__gte=six_months_ago, status__in=confirmed_product)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('product__price'))
    }
 
    chart_labels   = [m.strftime('%b %Y') for m in months]
    chart_homestay = [hs_d.get(m, 0)   for m in months]
    chart_package  = [pkg_d.get(m, 0)  for m in months]
    chart_product  = [prod_d.get(m, 0) for m in months]
    chart_total    = [a + b + c for a, b, c in zip(chart_homestay, chart_package, chart_product)]
 
    # ── Data chart kunjungan (count booking, HARUS sebelum mom_visitors_pct) ──
    hs_cnt  = monthly_count(HomestayBooking)
    pkg_cnt = monthly_count(PackageBooking)
    chart_visitors = [hs_cnt.get(m, 0) + pkg_cnt.get(m, 0) for m in months]
 
    # ── Data chart booking count homestay (untuk bar chart, bukan revenue) ────
    chart_homestay_count = [hs_cnt.get(m, 0) for m in months]  # reuse hs_cnt
 
    # ── MoM growth % (harus setelah semua chart_* terdefinisi) ───────────────
    def pct_change(current, previous):
        if (previous is None or previous == 0) and current > 0:
            return 100.0
        
        # Jika keduanya 0, maka memang 0%
        if (previous is None or previous == 0) and (current == 0):
            return 0.0
        
        return round(((current - previous) / previous) * 100, 1)
        
    mom_visitors_pct = pct_change(chart_visitors[-1],  chart_visitors[-2])  if len(chart_visitors)  >= 2 else 0
    mom_homestay_pct = pct_change(chart_homestay[-1],  chart_homestay[-2])  if len(chart_homestay)  >= 2 else 0
    mom_revenue_pct  = pct_change(chart_total[-1],     chart_total[-2])     if len(chart_total)     >= 2 else 0
    mom_product_pct  = pct_change(chart_product[-1],   chart_product[-2])   if len(chart_product)   >= 2 else 0
 
    # ── Top performers ────────────────────────────────────────────────────────
    top_homestays = (
        HomestayBooking.objects
        .filter(created_at__date__gte=date_from, created_at__date__lte=date_to,
                status__in=confirmed_other)
        .values('homestay__name')
        .annotate(total=Sum('total_price'), cnt=Count('id'))
        .order_by('-total')[:5]
    )
    top_packages = (
        PackageBooking.objects
        .filter(created_at__date__gte=date_from, created_at__date__lte=date_to,
                status__in=confirmed_other)
        .values('tour_package__name')
        .annotate(total=Sum('total_price'), cnt=Count('id'))
        .order_by('-total')[:5]
    )
 
    # ── Top products ──────────────────────────────────────────────────────────
    top_products = (
        ProductOrder.objects
        .filter(
            created_at__date__gte=date_from,
            created_at__date__lte=date_to,
            status__in=confirmed_product,
        )
        .values('product__name', 'product__category__name')
        .annotate(
            qty=Sum('quantity'),
            revenue=Sum(
                ExpressionWrapper(
                    F('quantity') * F('product__price'),
                    output_field=FloatField()
                )
            ),
        )
        .order_by('-qty')[:6]
    )
 
    # ── Rata-rata durasi menginap (malam) ─────────────────────────────────────
    hs_durations = list(
        HomestayBooking.objects
        .filter(created_at__date__gte=date_from, created_at__date__lte=date_to)
        .annotate(
            duration=ExpressionWrapper(
                F('check_out') - F('check_in'),
                output_field=DurationField()
            )
        )
        .values_list('duration', flat=True)
    )
    if hs_durations:
        total_days = sum(
            (d.days if d is not None and hasattr(d, 'days') else 0)
            for d in hs_durations
        )
        avg_stay_nights = round(total_days / len(hs_durations), 1)
    else:
        avg_stay_nights = 0
 
    # ── Customer satisfaction (avg rating semua review approved) ──────────────
    avg_rating_raw = Review.objects.filter(is_approved=True).aggregate(avg=Avg('rating'))['avg']
    avg_rating     = round(float(avg_rating_raw), 1) if avg_rating_raw else 0
 
    # ── Total kunjungan 6 bulan ───────────────────────────────────────────────
    total_six_months = sum(chart_visitors)
 
    # ── Repeat visitor rate ───────────────────────────────────────────────────
    hs_emails     = list(HomestayBooking.objects.values_list('email', flat=True))
    pkg_emails    = list(PackageBooking.objects.values_list('email', flat=True))
    email_counter = Counter(hs_emails + pkg_emails)
    repeat_count  = sum(1 for v in email_counter.values() if v > 1)
    total_unique  = len(email_counter)
    repeat_rate   = round((repeat_count / total_unique * 100), 1) if total_unique else 0
 
    # ── Target KPI progress ───────────────────────────────────────────────────
    TARGET_VISITORS = 200
    TARGET_HOMESTAY = 20
    visitor_pct  = min(round((total_visitors        / TARGET_VISITORS * 100), 1), 100)
    homestay_pct = min(round((breakdown[0]['count'] / TARGET_HOMESTAY * 100), 1), 100)
 
    # ── Ranking destinasi (dari PackageBooking) ───────────────────────────────
    dest_colors  = ['#22c55e', '#3b82f6', '#f59e0b', '#e11d48', '#8b5cf6']
    dest_qs_raw  = list(
        PackageBooking.objects
        .filter(created_at__date__gte=date_from, created_at__date__lte=date_to)
        .values('tour_package__name')
        .annotate(visits=Count('id'))
        .order_by('-visits')[:5]
    )
    max_visits   = dest_qs_raw[0]['visits'] if dest_qs_raw else 1
    dest_ranking = [
        {
            'name':   d['tour_package__name'] or 'Paket Tidak Diketahui',
            'visits': d['visits'],
            'pct':    round(d['visits'] / max_visits * 100, 1),
            'color':  dest_colors[i % len(dest_colors)],
        }
        for i, d in enumerate(dest_qs_raw)
    ]
 
    # ── Context ───────────────────────────────────────────────────────────────
    context = {
        'active_nav':   'analytics',
        'period':       period,
        'period_label': period_label,
        'date_from':    date_from.isoformat(),
        'date_to':      date_to.isoformat(),
 
        # KPI utama
        'total_visitors':     total_visitors,
        'total_revenue_fmt':  _fmt_rupiah(total_revenue),
        'total_transactions': total_transactions,
        'avg_revenue_fmt':    _fmt_rupiah(avg_revenue),
        'rev_homestay_fmt':   _fmt_rupiah(rev_homestay),
        'rev_product_fmt':    _fmt_rupiah(rev_product),
        'rev_package_fmt':    _fmt_rupiah(rev_package),
 
        # Breakdown cards
        'breakdown':     breakdown,
        'top_homestays': top_homestays,
        'top_packages':  top_packages,
        'top_products':  top_products,
 
        # Charts — revenue
        'chart_labels_json':   json.dumps(chart_labels),
        'chart_total_json':    json.dumps(chart_total),
        'chart_homestay_json': json.dumps(chart_homestay),
        'chart_package_json':  json.dumps(chart_package),
        'chart_product_json':  json.dumps(chart_product),
        'chart_visitors_json': json.dumps(chart_visitors),
 
        # Chart — booking count homestay (bar chart)
        'chart_homestay_count_json': json.dumps(chart_homestay_count),
 
        # Donut breakdown
        'donut_labels_json': json.dumps([b['label']   for b in breakdown]),
        'donut_data_json':   json.dumps([b['revenue'] for b in breakdown]),
        'donut_colors_json': json.dumps([b['color']   for b in breakdown]),
 
        # MoM growth %
        'mom_visitors_pct': mom_visitors_pct,
        'mom_homestay_pct': mom_homestay_pct,
        'mom_revenue_pct':  mom_revenue_pct,
        'mom_product_pct':  mom_product_pct,
 
        # Target KPI
        'visitor_pct':     visitor_pct,
        'homestay_pct':    homestay_pct,
        'target_visitors': TARGET_VISITORS,
        'target_homestay': TARGET_HOMESTAY,
 
        # Bottom stats
        'avg_stay_nights':  avg_stay_nights,
        'avg_rating':       avg_rating,
        'total_six_months': total_six_months,
        'repeat_rate':      repeat_rate,
 
        # Destinasi ranking
        'dest_ranking':     dest_ranking,
        'dest_labels_json': json.dumps([d['name']   for d in dest_ranking]),
        'dest_data_json':   json.dumps([d['visits'] for d in dest_ranking]),
        'dest_colors_json': json.dumps([d['color']  for d in dest_ranking]),
    }
    return render(request, 'dashboard/analytics.html', context)
 
 
# ════════════════════════════════════════════════════════════════════════════
#  EXPORT: EXCEL
# ════════════════════════════════════════════════════════════════════════════
 
def export_excel(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')
 
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
    except ImportError:
        return HttpResponse(
            "openpyxl tidak terinstall. Jalankan: pip install openpyxl", status=500)
 
    date_from, date_to, _, period_label = _parse_period(request)
    confirmed_product = ['confirmed', 'ready_pickup', 'shipping', 'completed']
    confirmed_other   = ['confirmed', 'completed']
 
    wb = openpyxl.Workbook()
 
    # ── shared styles ────────────────────────────────────────────────────
    H_FILL  = PatternFill("solid", fgColor="1a5276")
    H_FONT  = Font(color="FFFFFF", bold=True, size=11)
    ALT_FILL= PatternFill("solid", fgColor="d6eaf8")
    CENTER  = Alignment(horizontal='center', vertical='center')
    THIN    = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'),  bottom=Side(style='thin'),
    )
 
    def header_row(ws, row, n):
        for c in range(1, n + 1):
            cell = ws.cell(row=row, column=c)
            cell.fill, cell.font, cell.alignment, cell.border = H_FILL, H_FONT, CENTER, THIN
 
    def data_row(ws, row, n, alt=False):
        fill = ALT_FILL if alt else PatternFill("solid", fgColor="FFFFFF")
        for c in range(1, n + 1):
            cell = ws.cell(row=row, column=c)
            cell.fill   = fill
            cell.border = THIN
            cell.alignment = Alignment(vertical='center')
 
    def set_widths(ws, widths):
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
 
    # ── Sheet 1 – Ringkasan ──────────────────────────────────────────────
    ws1 = wb.active
    ws1.title = "Ringkasan"
    set_widths(ws1, [32, 26])
 
    ws1['A1'] = "LAPORAN KINERJA WISATA DESA MANUD JAYA"
    ws1['A1'].font = Font(bold=True, size=14)
    ws1['A1'].alignment = CENTER
    ws1.merge_cells('A1:B1')
    ws1['A2'] = f"Periode: {period_label}"
    ws1['A2'].font = Font(italic=True)
    ws1.merge_cells('A2:B2')
    ws1.append([])
 
    hs_qs  = HomestayBooking.objects.filter(
        created_at__date__gte=date_from, created_at__date__lte=date_to)
    pr_qs  = ProductOrder.objects.filter(
        created_at__date__gte=date_from, created_at__date__lte=date_to)
    pk_qs  = PackageBooking.objects.filter(
        created_at__date__gte=date_from, created_at__date__lte=date_to)
 
    rev_hs = hs_qs.filter(status__in=confirmed_other).aggregate(t=Sum('total_price'))['t'] or 0
    rev_pr = pr_qs.filter(status__in=confirmed_product).aggregate(t=Sum('product__price'))['t'] or 0
    rev_pk = pk_qs.filter(status__in=confirmed_other).aggregate(t=Sum('total_price'))['t'] or 0
    total_rev = rev_hs + rev_pr + rev_pk
 
    ws1.append(["Indikator", "Nilai"])
    header_row(ws1, 4, 2)
 
    rows = [
        ("Total Kunjungan Wisatawan", hs_qs.count() + pk_qs.count()),
        ("Total Transaksi",           hs_qs.count() + pr_qs.count() + pk_qs.count()),
        ("Total Pendapatan",          _fmt_rupiah(total_rev)),
        ("Pendapatan Homestay",       _fmt_rupiah(rev_hs)),
        ("Pendapatan Produk Lokal",   _fmt_rupiah(rev_pr)),
        ("Pendapatan Paket Wisata",   _fmt_rupiah(rev_pk)),
        ("Pemesanan Homestay",        hs_qs.count()),
        ("Pemesanan Produk",          pr_qs.count()),
        ("Pemesanan Paket Wisata",    pk_qs.count()),
    ]
    for i, (k, v) in enumerate(rows, 5):
        ws1.cell(row=i, column=1, value=k)
        ws1.cell(row=i, column=2, value=v)
        data_row(ws1, i, 2, alt=(i % 2 == 0))
 
    # ── Sheet 2 – Homestay Bookings ──────────────────────────────────────
    ws2 = wb.create_sheet("Pemesanan Homestay")
    cols = ["ID", "Nama Tamu", "Homestay", "Check-in", "Check-out", "Total Harga", "Status", "Tgl Pesan"]
    set_widths(ws2, [6, 25, 30, 14, 14, 20, 15, 22])
    ws2.append(cols)
    header_row(ws2, 1, len(cols))
    for i, b in enumerate(hs_qs.select_related('homestay').order_by('-created_at'), 2):
        ws2.append([b.pk, b.customer_name, b.homestay.name,
                    b.check_in.strftime('%d/%m/%Y'), b.check_out.strftime('%d/%m/%Y'),
                    float(b.total_price), b.get_status_display(),
                    b.created_at.strftime('%d/%m/%Y %H:%M')])
        data_row(ws2, i, len(cols), alt=(i % 2 == 0))
 
    # ── Sheet 3 – Product Orders ─────────────────────────────────────────
    ws3 = wb.create_sheet("Pesanan Produk")
    cols = ["ID", "Nama Pelanggan", "Produk", "Qty", "Harga Satuan", "Total", "Status", "Tgl Pesan"]
    set_widths(ws3, [6, 25, 30, 6, 18, 20, 15, 22])
    ws3.append(cols)
    header_row(ws3, 1, len(cols))
    for i, o in enumerate(pr_qs.select_related('product').order_by('-created_at'), 2):
        ws3.append([o.pk, o.customer_name, o.product.name, o.quantity,
                    float(o.product.price), float(o.product.price) * o.quantity,
                    o.get_status_display(), o.created_at.strftime('%d/%m/%Y %H:%M')])
        data_row(ws3, i, len(cols), alt=(i % 2 == 0))
 
    # ── Sheet 4 – Package Bookings ───────────────────────────────────────
    ws4 = wb.create_sheet("Pemesanan Paket Wisata")
    cols = ["ID", "Nama Tamu", "Paket", "Pemandu", "Tgl Tour", "Peserta", "Total Harga", "Status", "Tgl Pesan"]
    set_widths(ws4, [6, 25, 30, 25, 14, 8, 20, 15, 22])
    ws4.append(cols)
    header_row(ws4, 1, len(cols))
    for i, b in enumerate(pk_qs.select_related('tour_package', 'guide').order_by('-created_at'), 2):
        ws4.append([b.pk, b.customer_name, b.tour_package.name,
                    b.guide.name if b.guide else '-',
                    b.tour_date.strftime('%d/%m/%Y'), b.num_participants,
                    float(b.total_price), b.get_status_display(),
                    b.created_at.strftime('%d/%m/%Y %H:%M')])
        data_row(ws4, i, len(cols), alt=(i % 2 == 0))
 
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = (
        f'attachment; filename="laporan_wisata_{date_from}_{date_to}.xlsx"')
    wb.save(response)
    return response
 
 
# ════════════════════════════════════════════════════════════════════════════
#  EXPORT: PDF
# ════════════════════════════════════════════════════════════════════════════
 
def export_pdf(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')
 
    try:
        import io
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib.enums import TA_CENTER
        from reportlab.platypus import (
            SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable)
    except ImportError:
        return HttpResponse(
            "reportlab tidak terinstall. Jalankan: pip install reportlab", status=500)
 
    date_from, date_to, _, period_label = _parse_period(request)
    confirmed_product = ['confirmed', 'ready_pickup', 'shipping', 'completed']
    confirmed_other   = ['confirmed', 'completed']
 
    hs_qs = HomestayBooking.objects.filter(
        created_at__date__gte=date_from, created_at__date__lte=date_to)
    pr_qs = ProductOrder.objects.filter(
        created_at__date__gte=date_from, created_at__date__lte=date_to)
    pk_qs = PackageBooking.objects.filter(
        created_at__date__gte=date_from, created_at__date__lte=date_to)
 
    rev_hs = hs_qs.filter(status__in=confirmed_other).aggregate(t=Sum('total_price'))['t'] or 0
    rev_pr = pr_qs.filter(status__in=confirmed_product).aggregate(t=Sum('product__price'))['t'] or 0
    rev_pk = pk_qs.filter(status__in=confirmed_other).aggregate(t=Sum('total_price'))['t'] or 0
    total_rev = rev_hs + rev_pr + rev_pk
 
    BRAND  = colors.HexColor('#1a5276')
    ACCENT = colors.HexColor('#2e86c1')
    LIGHT  = colors.HexColor('#d6eaf8')
 
    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(buffer, pagesize=A4,
                                topMargin=2*cm, bottomMargin=2*cm,
                                leftMargin=2*cm, rightMargin=2*cm)
    styles = getSampleStyleSheet()
 
    title_s   = ParagraphStyle('T', parent=styles['Title'],
                                fontSize=18, textColor=BRAND, spaceAfter=4, alignment=TA_CENTER)
    sub_s     = ParagraphStyle('S', parent=styles['Normal'],
                                fontSize=10, textColor=colors.grey,
                                alignment=TA_CENTER, spaceAfter=16)
    section_s = ParagraphStyle('H', parent=styles['Heading2'],
                                fontSize=12, textColor=BRAND, spaceBefore=16, spaceAfter=8)
    footer_s  = ParagraphStyle('F', parent=styles['Normal'],
                                fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
 
    TS_BASE = [
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#aed6f1')),
        ('TOPPADDING',    (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING',   (0, 0), (-1, -1), 7),
    ]
 
    def make_table(data, col_widths, header_color=ACCENT):
        t = Table(data, colWidths=col_widths)
        t.setStyle(TableStyle(TS_BASE + [
            ('BACKGROUND', (0, 0), (-1, 0), header_color),
            ('TEXTCOLOR',  (0, 0), (-1, 0), colors.white),
            ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        return t
 
    story = [
        Paragraph("LAPORAN KINERJA WISATA", title_s),
        Paragraph("Desa Manud Jaya", title_s),
        Paragraph(f"Periode: {period_label}", sub_s),
        HRFlowable(width="100%", thickness=2, color=BRAND),
        Spacer(1, 0.4*cm),
    ]
 
    # KPI summary
    story.append(Paragraph("Ringkasan Kinerja", section_s))
    story.append(make_table([
        ["Indikator", "Nilai"],
        ["Total Kunjungan Wisatawan", str(hs_qs.count() + pk_qs.count())],
        ["Total Transaksi",           str(hs_qs.count() + pr_qs.count() + pk_qs.count())],
        ["Total Pendapatan",          _fmt_rupiah(total_rev)],
        ["Pendapatan Homestay",       _fmt_rupiah(rev_hs)],
        ["Pendapatan Produk Lokal",   _fmt_rupiah(rev_pr)],
        ["Pendapatan Paket Wisata",   _fmt_rupiah(rev_pk)],
    ], [10*cm, 7*cm], header_color=BRAND))
 
    # Homestay detail
    story.append(Paragraph("Detail Pemesanan Homestay (10 Terbaru)", section_s))
    hs_rows = [["Nama Tamu", "Homestay", "Check-in", "Check-out", "Total", "Status"]]
    for b in hs_qs.select_related('homestay').order_by('-created_at')[:10]:
        hs_rows.append([b.customer_name, b.homestay.name,
                         b.check_in.strftime('%d/%m/%Y'), b.check_out.strftime('%d/%m/%Y'),
                         _fmt_rupiah(b.total_price), b.get_status_display()])
    if len(hs_rows) == 1:
        hs_rows.append(["Tidak ada data", "-", "-", "-", "-", "-"])
    story.append(make_table(hs_rows, [3.5*cm, 4*cm, 2.5*cm, 2.5*cm, 3*cm, 2.5*cm]))
 
    # Package detail
    story.append(Paragraph("Detail Pemesanan Paket Wisata (10 Terbaru)", section_s))
    pk_rows = [["Nama Tamu", "Paket", "Tgl Tour", "Peserta", "Total", "Status"]]
    for b in pk_qs.select_related('tour_package').order_by('-created_at')[:10]:
        pk_rows.append([b.customer_name, b.tour_package.name,
                         b.tour_date.strftime('%d/%m/%Y'), str(b.num_participants),
                         _fmt_rupiah(b.total_price), b.get_status_display()])
    if len(pk_rows) == 1:
        pk_rows.append(["Tidak ada data", "-", "-", "-", "-", "-"])
    story.append(make_table(pk_rows, [3.5*cm, 4.5*cm, 2.5*cm, 2*cm, 3*cm, 2.5*cm]))
 
    story += [
        Spacer(1, 0.5*cm),
        HRFlowable(width="100%", thickness=1, color=colors.HexColor('#aed6f1')),
        Spacer(1, 0.2*cm),
        Paragraph(f"Laporan digenerate otomatis — {date.today().strftime('%d %B %Y')}", footer_s),
    ]
 
    doc.build(story)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="laporan_wisata_{date_from}_{date_to}.pdf"')
    return response