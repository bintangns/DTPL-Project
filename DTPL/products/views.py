from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductCategory
from .forms import ProductForm, ProductCategoryForm


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


# =========================
# ADMIN PAGES
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
