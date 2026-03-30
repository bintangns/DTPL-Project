from django import forms
from .models import Product, ProductCategory


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