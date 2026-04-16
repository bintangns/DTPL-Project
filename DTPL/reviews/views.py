from collections import defaultdict
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from destinations.models import Destination
from homestays.models import Homestay
from products.models import Product

from .forms import ReviewForm, AdminReplyForm
from .models import Review


MODEL_MAP = {
    'product': (Product, 'products:detail'),
    'homestay': (Homestay, 'homestays:detail'),
    'destination': (Destination, 'destinations:detail'),
}


def is_admin_logged_in(request):
    return request.session.get('is_admin_logged_in', False)


def create_review(request, content_type, slug):
    model_config = MODEL_MAP.get(content_type)
    if not model_config:
        messages.error(request, 'Tipe ulasan tidak valid.')
        return redirect('/')

    model_class, redirect_name = model_config
    instance = get_object_or_404(model_class, slug=slug)

    if request.method != 'POST':
        return redirect(redirect_name, slug=slug)

    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.content_type = ContentType.objects.get_for_model(model_class)
        review.object_id = instance.pk
        review.save()
        messages.success(request, 'Terima kasih, ulasan Anda berhasil dikirim.')
    else:
        messages.error(request, 'Gagal mengirim ulasan. Periksa form Anda.')

    return redirect(redirect_name, slug=slug)


def admin_review_list(request):
    if not is_admin_logged_in(request):
        return redirect('adminpanel:login')

    product_ct = ContentType.objects.get_for_model(Product)
    destination_ct = ContentType.objects.get_for_model(Destination)
    homestay_ct = ContentType.objects.get_for_model(Homestay)

    product_reviews = Review.objects.filter(content_type=product_ct).select_related('content_type')
    destination_reviews = Review.objects.filter(content_type=destination_ct).select_related('content_type')
    homestay_reviews = Review.objects.filter(content_type=homestay_ct).select_related('content_type')

    grouped_products = defaultdict(list)
    grouped_destinations = defaultdict(list)
    grouped_homestays = defaultdict(list)

    for review in product_reviews:
        item_name = review.content_object.name if review.content_object else 'Item tidak ditemukan'
        grouped_products[item_name].append(review)

    for review in destination_reviews:
        item_name = review.content_object.name if review.content_object else 'Item tidak ditemukan'
        grouped_destinations[item_name].append(review)

    for review in homestay_reviews:
        item_name = review.content_object.name if review.content_object else 'Item tidak ditemukan'
        grouped_homestays[item_name].append(review)

    return render(request, 'reviews/admin_review_list.html', {
        'grouped_products': dict(grouped_products),
        'grouped_destinations': dict(grouped_destinations),
        'grouped_homestays': dict(grouped_homestays),
    })


def approve_review(request, review_id):
    if not is_admin_logged_in(request):
        return redirect('adminpanel:login')

    review = get_object_or_404(Review, id=review_id)
    review.is_approved = True
    review.save()

    messages.success(request, 'Review berhasil di-approve.')
    return redirect('reviews:admin_list')


def delete_review(request, review_id):
    if not is_admin_logged_in(request):
        return redirect('adminpanel:login')

    review = get_object_or_404(Review, id=review_id)
    review.delete()

    messages.success(request, 'Review berhasil dihapus.')
    return redirect('reviews:admin_list')


def reply_review(request, review_id):
    if not is_admin_logged_in(request):
        return redirect('adminpanel:login')

    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        form = AdminReplyForm(request.POST, instance=review)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.replied_at = timezone.now()
            reply.save()
            messages.success(request, 'Balasan review berhasil disimpan.')
            return redirect('reviews:admin_list')
    else:
        form = AdminReplyForm(instance=review)

    return render(request, 'reviews/admin_reply_review.html', {
        'review': review,
        'form': form,
    })