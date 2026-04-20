from django.contrib import admin
from .models import Guide, TourPackage, PackageBooking


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'languages', 'is_available', 'created_at')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'languages')


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'price_local', 'price_international', 'is_active')
    list_filter = ('is_active', 'destination')
    search_fields = ('name',)


@admin.register(PackageBooking)
class PackageBookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'tour_package', 'guide', 'tour_date', 'status', 'total_price')
    list_filter = ('status', 'tourist_category')
    search_fields = ('customer_name', 'email')
