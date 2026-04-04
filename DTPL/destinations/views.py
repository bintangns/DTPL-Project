from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from .models import Destination, DestinationCategory
from .forms import DestinationForm


# =========================
# PUBLIC PAGES
# =========================
def destination_list(request):
    """Render the destination landing page with all active destinations."""
    destinations = Destination.objects.filter(
        is_active=True,
    ).select_related('category')
    context = {'destinations': destinations}
    return render(request, 'destinations/index.html', context)


def destination_detail(request, slug):
    """Render a single destination detail page by slug."""
    destination = get_object_or_404(
        Destination.objects.select_related('category'),
        slug=slug,
        is_active=True,
    )
    context = {'dest': destination}
    return render(request, 'destinations/detail.html', context)


# =========================
# ADMIN — DESTINATION CRUD
# =========================
def admin_destination_list(request):
    """Admin dashboard: list all destinations with stats and search."""
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    query = request.GET.get('q', '').strip()
    destinations = Destination.objects.select_related('category').all()

    if query:
        destinations = destinations.filter(
            Q(name__icontains=query)
            | Q(location__icontains=query)
            | Q(category__name__icontains=query)
        )

    # Stats
    all_destinations = Destination.objects.select_related('category').all()
    total_destinations = all_destinations.count()
    total_alam = all_destinations.filter(category__name='Alam').count()
    total_budaya = all_destinations.filter(category__name='Budaya').count()
    total_eco = all_destinations.filter(is_eco_friendly=True).count()

    context = {
        'active_nav': 'destinasi',
        'destinations': destinations,
        'total_destinations': total_destinations,
        'total_alam': total_alam,
        'total_budaya': total_budaya,
        'total_eco': total_eco,
        'search_query': query,
    }
    return render(request, 'destinations/admin_dashboard.html', context)


def admin_destination_create(request):
    """Admin: create a new destination."""
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    if request.method == 'POST':
        form = DestinationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('destinations_admin:list')
    else:
        form = DestinationForm()

    categories = DestinationCategory.objects.all()
    return render(request, 'destinations/admin_destination_form.html', {
        'active_nav': 'destinasi',
        'form': form,
        'categories': categories,
        'page_title': 'Tambah Destinasi',
        'submit_label': 'Simpan Destinasi',
    })


def admin_destination_edit(request, pk):
    """Admin: edit an existing destination."""
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    destination = get_object_or_404(Destination, pk=pk)

    if request.method == 'POST':
        form = DestinationForm(request.POST, instance=destination)
        if form.is_valid():
            form.save()
            return redirect('destinations_admin:list')
    else:
        form = DestinationForm(instance=destination)

    categories = DestinationCategory.objects.all()
    return render(request, 'destinations/admin_destination_form.html', {
        'active_nav': 'destinasi',
        'form': form,
        'categories': categories,
        'destination': destination,
        'page_title': 'Edit Destinasi',
        'submit_label': 'Simpan Perubahan',
    })


def admin_destination_delete(request, pk):
    """Admin: delete a destination (with confirmation page)."""
    if not request.session.get('is_admin_logged_in'):
        return redirect('adminpanel:login')

    destination = get_object_or_404(Destination, pk=pk)

    if request.method == 'POST':
        destination.delete()
        return redirect('destinations_admin:list')

    return render(request, 'destinations/admin_destination_delete.html', {
        'active_nav': 'destinasi',
        'destination': destination,
    })
