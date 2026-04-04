from django.db import models
from django.contrib.auth.models import User
import json

from django.db import models
from django.utils.text import slugify

class Homestay(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    owner = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    
    price_per_night = models.DecimalField(
        max_digits=12, 
        decimal_places=2
    )
    
    capacity = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    image_url = models.URLField(blank=True)
    address = models.TextField()
    
    facilities = models.TextField(default="[]", blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Otomatisasi slug berdasarkan nama homestay
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_facilities_list(self):
        try:
            return json.loads(self.facilities)
        except json.JSONDecodeError:
            return []

    def __str__(self):
        return self.name

class HomestayBooking(models.Model):
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

    homestay = models.ForeignKey(
        Homestay, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    customer_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    
    check_in = models.DateField()
    check_out = models.DateField()
    payment_proof = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)
    
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=STATUS_PENDING
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Menghitung total harga: (Check-out - Check-in) * Harga per malam
        if self.check_in and self.check_out:
            duration = (self.check_out - self.check_in).days
            if duration > 0:
                self.total_price = self.homestay.price_per_night * duration
            else:
                self.total_price = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.homestay.name} - {self.customer_name}"