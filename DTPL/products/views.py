from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProductForm, ProductCategoryForm, ProductOrderForm
from .models import Product, ProductCategory, ProductOrder


# =========================
# EMAIL HELPER
# =========================
def send_order_status_email(order, subject, message):
    if order.email:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
            recipient_list=[order.email],
            fail_silently=False,
        )


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
        form = ProductOrderForm(request.POST)
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
                f'Email: {order.email}\n'
                f'No. Telepon: {order.phone_number}\n'
                f'Alamat: {order.address}\n'
                f'Status: Pending\n\n'
                f'Pesanan Anda sedang kami proses.'
            )
            send_order_status_email(order, subject, message)

            return redirect('products:order_success', pk=order.pk)
    else:
        form = ProductOrderForm()

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

    categories = ProductCategory.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
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
        'category': category,
    })


# =========================
# ADMIN ORDER
# =========================
def admin_order_list(request):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    orders = ProductOrder.objects.select_related('product').all()

    return render(request, 'products/admin_order_list.html', {
        'orders': orders,
    })


def admin_order_detail(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    order = get_object_or_404(ProductOrder.objects.select_related('product'), pk=pk)

    return render(request, 'products/admin_order_detail.html', {
        'order': order,
    })


def admin_order_confirm(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    order = get_object_or_404(ProductOrder, pk=pk)
    order.status = ProductOrder.STATUS_CONFIRMED
    order.save()

    send_order_status_email(
        order,
        'Pesanan Anda Telah Dikonfirmasi',
        (
            f'Halo {order.customer_name},\n\n'
            f'Pesanan Anda untuk produk {order.product.name} telah dikonfirmasi.\n'
            f'Status saat ini: Confirmed.\n\n'
            f'Terima kasih.'
        )
    )
    return redirect('products_admin:order_detail', pk=order.pk)


def admin_order_shipping(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    order = get_object_or_404(ProductOrder, pk=pk)
    order.status = ProductOrder.STATUS_SHIPPING
    order.save()

    send_order_status_email(
        order,
        'Pesanan Anda Sedang Diantar',
        (
            f'Halo {order.customer_name},\n\n'
            f'Pesanan Anda untuk produk {order.product.name} sedang diantar.\n'
            f'Status saat ini: Shipping.\n\n'
            f'Terima kasih.'
        )
    )
    return redirect('products_admin:order_detail', pk=order.pk)


def admin_order_complete(request, pk):
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    order = get_object_or_404(ProductOrder, pk=pk)
    order.status = ProductOrder.STATUS_COMPLETED
    order.save()

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
    return redirect('products_admin:order_detail', pk=order.pk)