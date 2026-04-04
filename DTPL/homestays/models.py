from django.db import models
from django.contrib.auth.models import User


class Facility(models.Model):
    name = models.CharField(max_length=100)


class Homestay(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    owner = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    capacity = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    image_url = models.URLField(blank=True)
    address = models.TextField()

    facilities = models.ManyToManyField(
        Facility,
        related_name="homestays",
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)