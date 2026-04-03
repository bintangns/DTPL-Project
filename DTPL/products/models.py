from django.db import models
from django.utils.text import slugify


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name='products'
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    short_description = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
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


class ProductOrder(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_READY_PICKUP = 'ready_pickup'
    STATUS_SHIPPING = 'shipping'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_READY_PICKUP, 'Ready for Pickup'),
        (STATUS_SHIPPING, 'Shipping'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    METHOD_PICKUP = 'pickup'
    METHOD_DELIVERY = 'delivery'
    FULFILLMENT_CHOICES = [
        (METHOD_PICKUP, 'Pengambilan di Toko Pusat Oleh-Oleh Desa'),
        (METHOD_DELIVERY, 'Dikirim ke Alamat Pemesan'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='orders'
    )
    customer_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    quantity = models.PositiveIntegerField(default=1)

    fulfillment_method = models.CharField(
        max_length=20,
        choices=FULFILLMENT_CHOICES,
        default=METHOD_PICKUP
    )

    address = models.TextField(blank=True)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    notes = models.TextField(blank=True)
    payment_proof = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    stock_deducted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk} - {self.customer_name} - {self.product.name}'