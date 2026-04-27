from django import forms
from django.core.exceptions import ValidationError
from .models import Homestay, HomestayBooking
import re

class HomestayForm(forms.ModelForm):
    class Meta:
        model = Homestay
        fields = '__all__'

class PublicBookingForm(forms.ModelForm):
    class Meta:
        model = HomestayBooking
        fields = ['customer_name', 'email', 'phone_number', 'check_in', 'check_out', 'payment_proof', 'notes']
        
    def clean_customer_name(self):
        name = self.cleaned_data.get('customer_name')
        # Memastikan hanya huruf dan spasi yang diperbolehkan
        if not re.match(r'^[a-zA-Z\s]+$', name):
            raise ValidationError("Nama hanya boleh mengandung huruf.")
        return name

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        # Memastikan hanya angka yang diperbolehkan
        if not phone.isdigit():
            raise ValidationError("Nomor telepon hanya boleh mengandung angka.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        # Validasi logika tanggal: Check-out tidak boleh sebelum Check-in
        if check_in and check_out:
            if check_out <= check_in:
                raise ValidationError("Tanggal check-out harus setelah tanggal check-in.")
        return cleaned_data