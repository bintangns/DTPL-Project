from django import forms
from .models import Product, ProductCategory, ProductOrder


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'price',
            'stock',
            'short_description',
            'description',
            'image_url',
            'is_active',
        ]

class ProductOrderForm(forms.ModelForm):
    class Meta:
        model = ProductOrder
        fields = [
            'customer_name',
            'email',
            'phone_number',
            'quantity',
            'address',
            'notes',
        ]