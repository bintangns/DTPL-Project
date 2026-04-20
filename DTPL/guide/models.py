from django.db import models
from django.utils.text import slugify
from destinations.models import Destination


class Guide(models.Model):
    CATEGORY_LOCAL = 'lokal'
    CATEGORY_INTERNATIONAL = 'internasional'
    CATEGORY_CHOICES = [
        (CATEGORY_LOCAL, 'Lokal'),
        (CATEGORY_INTERNATIONAL, 'Internasional'),
    ]

    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_LOCAL)
    languages = models.CharField(
        max_length=255,
        help_text='Pisahkan dengan koma, contoh: Indonesia, English, Japanese'
    )
    profile_picture = models.ImageField(upload_to='guides/', blank=True, null=True)
    phone_number = models.CharField(max_length=30)
    email = models.EmailField()
    bio = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    @property
    def languages_list(self):
        """Return languages as a list, splitting by comma."""
        if self.languages:
            return [lang.strip() for lang in self.languages.split(',') if lang.strip()]
        return []


class TourPackage(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='tour_packages'
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    itinerary = models.TextField(blank=True, help_text='Agenda kegiatan wisata')
    price_local = models.DecimalField(
        max_digits=12, decimal_places=2,
        help_text='Harga untuk wisatawan lokal (IDR)'
    )
    price_international = models.DecimalField(
        max_digits=12, decimal_places=2,
        help_text='Harga untuk wisatawan mancanegara (IDR)'
    )
    image_url = models.URLField(blank=True)
    duration = models.CharField(max_length=50, help_text='Contoh: 4 Jam, Full Day')
    max_participants = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} — {self.destination.name}"


class PackageBooking(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    TOURIST_LOCAL = 'lokal'
    TOURIST_INTERNATIONAL = 'mancanegara'
    TOURIST_CHOICES = [
        (TOURIST_LOCAL, 'Lokal'),
        (TOURIST_INTERNATIONAL, 'Mancanegara'),
    ]

    tour_package = models.ForeignKey(
        TourPackage,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    guide = models.ForeignKey(
        Guide,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='bookings'
    )
    customer_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    tourist_category = models.CharField(
        max_length=20,
        choices=TOURIST_CHOICES,
        default=TOURIST_LOCAL
    )
    tour_date = models.DateField()
    start_time = models.TimeField()
    num_participants = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    payment_proof = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Auto-calculate total price based on tourist category
        if self.tour_package_id:
            if self.tourist_category == self.TOURIST_INTERNATIONAL:
                self.total_price = self.tour_package.price_international * self.num_participants
            else:
                self.total_price = self.tour_package.price_local * self.num_participants
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.pk} — {self.customer_name} — {self.tour_package.name}"
