from django import forms
from .models import Guide, TourPackage, PackageBooking


class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = [
            'name', 'slug', 'category', 'languages', 'profile_picture',
            'phone_number', 'email', 'bio', 'is_available',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama lengkap pemandu',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'auto-generated dari nama',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'languages': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Indonesia, English, Japanese',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0812...',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Deskripsi singkat pengalaman pemandu',
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'name': 'Nama Pemandu',
            'slug': 'Slug (URL)',
            'category': 'Kategori',
            'languages': 'Bahasa (pisahkan dengan koma)',
            'profile_picture': 'Foto Profil',
            'phone_number': 'No. Telepon / WhatsApp',
            'email': 'Email',
            'bio': 'Bio / Pengalaman',
            'is_available': 'Status Tersedia',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['bio'].required = False


class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = [
            'destination', 'name', 'slug', 'description', 'itinerary',
            'price_local', 'price_international', 'image_url',
            'duration', 'max_participants', 'is_active',
        ]
        widgets = {
            'destination': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama paket wisata',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'auto-generated dari nama',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Deskripsi lengkap paket wisata',
            }),
            'itinerary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '08:00 - Kumpul di basecamp\n09:00 - Mulai trekking\n...',
            }),
            'price_local': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '150000',
            }),
            'price_international': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '350000',
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://images.unsplash.com/...',
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '4 Jam / Full Day',
            }),
            'max_participants': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'destination': 'Destinasi',
            'name': 'Nama Paket',
            'slug': 'Slug (URL)',
            'description': 'Deskripsi',
            'itinerary': 'Itinerary / Agenda',
            'price_local': 'Harga Lokal (IDR)',
            'price_international': 'Harga Mancanegara (IDR)',
            'image_url': 'URL Foto',
            'duration': 'Durasi',
            'max_participants': 'Maks. Peserta',
            'is_active': 'Aktif',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['image_url'].required = False


class PackageBookingForm(forms.ModelForm):
    """Form yang diakses publik oleh wisatawan."""
    class Meta:
        model = PackageBooking
        fields = [
            'customer_name', 'email', 'phone_number',
            'tourist_category', 'tour_date', 'start_time',
            'num_participants', 'payment_proof', 'notes',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama lengkap Anda',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0812...',
            }),
            'tourist_category': forms.RadioSelect(),
            'tour_date': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'id': 'tour_date_picker',
                'readonly': 'readonly',
                'placeholder': 'Pilih tanggal',
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'num_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1',
            }),
            'payment_proof': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ada permintaan khusus?',
            }),
        }
        labels = {
            'customer_name': 'Nama Lengkap',
            'email': 'Email',
            'phone_number': 'No. Telepon (WhatsApp)',
            'tourist_category': 'Kategori Wisatawan',
            'tour_date': 'Tanggal Wisata',
            'start_time': 'Jam Mulai',
            'num_participants': 'Jumlah Peserta',
            'payment_proof': 'Bukti Pembayaran',
            'notes': 'Catatan Tambahan',
        }
