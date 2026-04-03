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
            'fulfillment_method',
            'address',
            'notes',
            'payment_proof',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'admin-form-input'}),
            'email': forms.EmailInput(attrs={'class': 'admin-form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'admin-form-input'}),
            'quantity': forms.NumberInput(attrs={'class': 'admin-form-input', 'min': 1}),
            'fulfillment_method': forms.Select(attrs={'class': 'admin-form-input'}),
            'address': forms.Textarea(attrs={'class': 'admin-form-input', 'rows': 4}),
            'notes': forms.Textarea(attrs={'class': 'admin-form-input', 'rows': 3}),
            'payment_proof': forms.ClearableFileInput(attrs={'class': 'admin-form-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

        if self.product:
            self.fields['quantity'].widget.attrs['max'] = self.product.stock
            self.fields['quantity'].help_text = f'Stok tersedia: {self.product.stock}'

    def clean(self):
        cleaned_data = super().clean()
        fulfillment_method = cleaned_data.get('fulfillment_method')
        address = cleaned_data.get('address')
        quantity = cleaned_data.get('quantity')

        if fulfillment_method == ProductOrder.METHOD_DELIVERY and not address:
            self.add_error('address', 'Alamat wajib diisi jika memilih pengiriman.')

        if self.product and quantity:
            if quantity < 1:
                self.add_error('quantity', 'Jumlah pesanan minimal 1.')
            elif quantity > self.product.stock:
                self.add_error(
                    'quantity',
                    f'Jumlah pesanan melebihi stok tersedia. Stok saat ini hanya {self.product.stock}.'
                )

        return cleaned_data