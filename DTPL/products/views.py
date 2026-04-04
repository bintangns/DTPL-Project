from django.conf import settings
from django.db import models
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
import requests



from .forms import ProductForm, ProductCategoryForm, ProductOrderForm
from .models import Product, ProductCategory, ProductOrder


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

def can_transition_order(order, new_status):
    allowed_transitions = {
        ProductOrder.STATUS_PENDING: [
            ProductOrder.STATUS_CONFIRMED,
            ProductOrder.STATUS_CANCELLED,
        ],
        ProductOrder.STATUS_CONFIRMED: [
            ProductOrder.STATUS_READY_PICKUP,
            ProductOrder.STATUS_SHIPPING,
            ProductOrder.STATUS_CANCELLED,
        ],
        ProductOrder.STATUS_READY_PICKUP: [
            ProductOrder.STATUS_COMPLETED,
        ],
        ProductOrder.STATUS_SHIPPING: [
            ProductOrder.STATUS_COMPLETED,
        ],
        ProductOrder.STATUS_COMPLETED: [],
        ProductOrder.STATUS_CANCELLED: [],
    }
    return new_status in allowed_transitions.get(order.status, [])

# =========================
# PUBLIC PAGES
# =========================
def product_list(request):
    category_slug = request.GET.get('category')

    products = Product.objects.filter(is_active=True).select_related('category')

    if category_slug:
        products = products.filter(category__slug=category_slug)

    categories = ProductCategory.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category'),
        slug=slug,
        is_active=True
    )
    return render(request, 'products/product_detail.html', {'product': product})


def product_order_create(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category'),
        slug=slug,
        is_active=True
    )

    if request.method == 'POST':
        form = ProductOrderForm(request.POST, request.FILES, product=product)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.status = ProductOrder.STATUS_PENDING
            order.save()

            subject = 'Pesanan Anda Telah Diterima'
            message = (
                f'Halo {order.customer_name},\n\n'
                f'Terima kasih, pesanan Anda telah kami terima.\n\n'
                f'Detail pesanan:\n'
                f'Produk: {order.product.name}\n'
                f'Jumlah: {order.quantity}\n'
                f'Metode: {order.get_fulfillment_method_display()}\n'
                f'Email: {order.email}\n'
                f'No. Telepon: {order.phone_number}\n'
                f'Alamat: {order.address if order.address else "-"}\n'
                f'Status: Pending\n\n'
                f'Pesanan Anda sedang kami proses.'
            )
            send_order_status_email(order, subject, message)

            return redirect('products:order_success', pk=order.pk)
    else:
        form = ProductOrderForm(product=product)

    return render(request, 'products/order_form.html', {
        'product': product,
        'form': form,
    })


def product_order_success(request, pk):
    order = get_object_or_404(ProductOrder.objects.select_related('product'), pk=pk)
    return render(request, 'products/order_success.html', {
        'order': order,
    })


# =========================
# ADMIN PRODUCT
# =========================
def admin_product_list(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    category_slug = request.GET.get('category')
    products = Product.objects.select_related('category').all()

    if category_slug:
        products = products.filter(category__slug=category_slug)

    categories = ProductCategory.objects.annotate(
        product_count=models.Count('products')
    ).all()
    total_products = Product.objects.count()
    total_stock = Product.objects.aggregate(total=models.Sum('stock'))['total'] or 0

    context = {
        'active_nav': 'produk',
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
        'total_products': total_products,
        'total_stock': total_stock,
    }
    return render(request, 'products/admin_dashboard.html', context)


def admin_product_create(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products_admin:list')
    else:
        form = ProductForm()

    return render(request, 'products/admin_product_form.html', {
        'active_nav': 'produk',
        'form': form,
        'page_title': 'Tambah Produk',
        'submit_label': 'Simpan Produk',
    })


def admin_product_edit(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products_admin:list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/admin_product_form.html', {
        'active_nav': 'produk',
        'form': form,
        'page_title': 'Edit Produk',
        'submit_label': 'Update Produk',
    })


def admin_product_delete(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('products_admin:list')

    return render(request, 'products/admin_product_delete.html', {
        'active_nav': 'produk',
        'product': product,
    })


# =========================
# ADMIN CATEGORY
# =========================
def admin_category_list(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    categories = ProductCategory.objects.all()
    return render(request, 'products/admin_category_list.html', {
        'active_nav': 'produk',
        'categories': categories,
    })


def admin_category_create(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products_admin:category_list')
    else:
        form = ProductCategoryForm()

    return render(request, 'products/admin_category_form.html', {
        'active_nav': 'produk',
        'form': form,
        'page_title': 'Tambah Category',
        'submit_label': 'Simpan Category',
    })


def admin_category_edit(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('products_admin:category_list')
    else:
        form = ProductCategoryForm(instance=category)

    return render(request, 'products/admin_category_form.html', {
        'active_nav': 'produk',
        'form': form,
        'page_title': 'Edit Category',
        'submit_label': 'Update Category',
    })


def admin_category_delete(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category.delete()
        return redirect('products_admin:category_list')

    return render(request, 'products/admin_category_delete.html', {
        'active_nav': 'produk',
        'category': category,
    })


# =========================
# ADMIN ORDER
# =========================
def admin_order_list(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    orders = ProductOrder.objects.select_related('product').all()
    total_orders = orders.count()
    orders_pending = orders.filter(status=ProductOrder.STATUS_PENDING).count()
    orders_confirmed = orders.filter(status=ProductOrder.STATUS_CONFIRMED).count()
    orders_completed = orders.filter(status=ProductOrder.STATUS_COMPLETED).count()

    return render(request, 'products/admin_order_list.html', {
        'active_nav': 'pemesanan_produk',
        'orders': orders,
        'total_orders': total_orders,
        'orders_pending': orders_pending,
        'orders_confirmed': orders_confirmed,
        'orders_completed': orders_completed,
    })


def admin_order_detail(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    order = get_object_or_404(ProductOrder.objects.select_related('product'), pk=pk)

    return render(request, 'products/admin_order_detail.html', {
        'active_nav': 'pemesanan_produk',
        'order': order,
    })


def admin_order_confirm(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    if request.method != 'POST':
        return redirect('products_admin:order_detail', pk=pk)

    order = get_object_or_404(ProductOrder.objects.select_related('product'), pk=pk)

    if not can_transition_order(order, ProductOrder.STATUS_CONFIRMED):
        messages.error(request, 'Status pesanan tidak bisa diubah ke Konfirmasi.')
        return redirect('products_admin:order_detail', pk=order.pk)

    if not order.stock_deducted:
        if order.product.stock < order.quantity:
            messages.error(request, 'Stok produk tidak mencukupi untuk mengonfirmasi pesanan ini.')
            return redirect('products_admin:order_detail', pk=order.pk)

        order.product.stock -= order.quantity
        order.product.save()
        order.stock_deducted = True

    order.status = ProductOrder.STATUS_CONFIRMED
    order.save()

    try:
        extra_message = ''
        if order.fulfillment_method == ProductOrder.METHOD_PICKUP:
            extra_message = '\nPesanan Anda akan disiapkan untuk diambil di toko pusat oleh-oleh desa.'
        else:
            extra_message = '\nPesanan Anda telah dikonfirmasi dan akan diproses untuk pengiriman.'

        send_order_status_email(
            order,
            'Pesanan Anda Telah Dikonfirmasi',
            (
                f'Halo {order.customer_name},\n\n'
                f'Pesanan Anda untuk produk {order.product.name} telah dikonfirmasi.\n'
                f'Status saat ini: Confirmed.\n'
                f'Metode: {order.get_fulfillment_method_display()}\n'
                f'Ongkir: Rp {order.shipping_cost if order.shipping_cost else 0}\n'
                f'{extra_message}\n\n'
                f'Terima kasih.'
            )
        )
        messages.success(request, 'Pesanan berhasil dikonfirmasi dan email berhasil dikirim.')
    except Exception as e:
        messages.warning(request, f'Pesanan berhasil dikonfirmasi, tapi email gagal dikirim: {e}')

    return redirect('products_admin:order_detail', pk=order.pk)

def admin_order_shipping(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    if request.method != 'POST':
        return redirect('products_admin:order_detail', pk=pk)

    order = get_object_or_404(ProductOrder, pk=pk)

    if order.fulfillment_method != ProductOrder.METHOD_DELIVERY:
        messages.error(request, 'Pesanan ini bukan untuk pengiriman.')
        return redirect('products_admin:order_detail', pk=order.pk)

    if not can_transition_order(order, ProductOrder.STATUS_SHIPPING):
        messages.error(request, 'Status pesanan tidak bisa diubah ke Sedang Diantar.')
        return redirect('products_admin:order_detail', pk=order.pk)

    order.status = ProductOrder.STATUS_SHIPPING
    order.save()

    try:
        send_order_status_email(
            order,
            'Pesanan Anda Sedang Diantar',
            (
                f'Halo {order.customer_name},\n\n'
                f'Pesanan Anda untuk produk {order.product.name} sedang diantar.\n'
                f'Alamat pengiriman: {order.address}\n'
                f'Estimasi biaya pengiriman: Rp {order.shipping_cost if order.shipping_cost else 0}\n\n'
                f'Terima kasih.'
            )
        )
        messages.success(request, 'Status pesanan berhasil diubah ke Sedang Diantar dan email berhasil dikirim.')
    except Exception as e:
        messages.warning(request, f'Status berhasil diubah, tapi email gagal dikirim: {e}')

    return redirect('products_admin:order_detail', pk=order.pk)

def admin_order_ready_pickup(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    if request.method != 'POST':
        return redirect('products_admin:order_detail', pk=pk)

    order = get_object_or_404(ProductOrder, pk=pk)

    if order.fulfillment_method != ProductOrder.METHOD_PICKUP:
        messages.error(request, 'Pesanan ini bukan untuk pengambilan di tempat.')
        return redirect('products_admin:order_detail', pk=order.pk)

    if not can_transition_order(order, ProductOrder.STATUS_READY_PICKUP):
        messages.error(request, 'Status pesanan tidak bisa diubah ke Siap Diambil.')
        return redirect('products_admin:order_detail', pk=order.pk)

    order.status = ProductOrder.STATUS_READY_PICKUP
    order.save()

    try:
        send_order_status_email(
            order,
            'Pesanan Anda Siap Diambil',
            (
                f'Halo {order.customer_name},\n\n'
                f'Pesanan Anda untuk produk {order.product.name} sudah siap diambil.\n'
                f'Silakan ambil di toko pusat oleh-oleh desa.\n\n'
                f'Terima kasih.'
            )
        )
        messages.success(request, 'Status pesanan berhasil diubah ke Siap Diambil dan email berhasil dikirim.')
    except Exception as e:
        messages.warning(request, f'Status berhasil diubah, tapi email gagal dikirim: {e}')

    return redirect('products_admin:order_detail', pk=order.pk)


def admin_order_complete(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    if request.method != 'POST':
        return redirect('products_admin:order_detail', pk=pk)

    order = get_object_or_404(ProductOrder, pk=pk)

    if not can_transition_order(order, ProductOrder.STATUS_COMPLETED):
        messages.error(request, 'Status pesanan tidak bisa diubah ke Selesai.')
        return redirect('products_admin:order_detail', pk=order.pk)

    order.status = ProductOrder.STATUS_COMPLETED
    order.save()

    try:
        send_order_status_email(
            order,
            'Pesanan Anda Telah Selesai',
            (
                f'Halo {order.customer_name},\n\n'
                f'Pesanan Anda untuk produk {order.product.name} telah selesai.\n'
                f'Status saat ini: Completed.\n\n'
                f'Terima kasih.'
            )
        )
        messages.success(request, 'Status pesanan berhasil diubah ke Selesai dan email berhasil dikirim.')
    except Exception as e:
        messages.warning(request, f'Status berhasil diubah, tapi email gagal dikirim: {e}')

    return redirect('products_admin:order_detail', pk=order.pk)