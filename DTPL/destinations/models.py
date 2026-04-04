from django.db import models
from django.utils.text import slugify


class DestinationCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Destination Category'
        verbose_name_plural = 'Destination Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Destination(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        DestinationCategory,
        on_delete=models.PROTECT,
        related_name='destinations',
    )
    location = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    duration = models.CharField(max_length=50, blank=True)
    difficulty = models.CharField(max_length=50, blank=True)
    best_time = models.CharField(max_length=100, blank=True)
    features = models.TextField(blank=True, help_text='Pisahkan dengan koma')
    activities = models.TextField(blank=True, help_text='Pisahkan dengan koma')
    is_eco_friendly = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def features_list(self):
        """Return features as a list, splitting by comma."""
        if self.features:
            return [f.strip() for f in self.features.split(',') if f.strip()]
        return []

    @property
    def activities_list(self):
        """Return activities as a list, splitting by comma."""
        if self.activities:
            return [a.strip() for a in self.activities.split(',') if a.strip()]
        return []
