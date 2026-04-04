from django import forms
from .models import Homestay, HomestayBooking

class HomestayForm(forms.ModelForm):
    class Meta:
        model = Homestay
        fields = '__all__'

class PublicBookingForm(forms.ModelForm):
    class Meta:
        model = HomestayBooking
        fields = ['customer_name', 'email', 'phone_number', 'check_in', 'check_out', 'payment_proof', 'notes']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ada permintaan khusus?', 'class': 'form-control'}),
        }