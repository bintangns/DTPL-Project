from django import forms
from .models import Destination, DestinationCategory


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = [
            'name', 'slug', 'category', 'location',
            'short_description', 'description', 'image_url',
            'duration', 'difficulty', 'best_time',
            'features', 'activities', 'is_eco_friendly',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama destinasi',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'auto-generated dari nama',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dusun ..., X km dari pusat desa',
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Deskripsi singkat untuk kartu destinasi',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Deskripsi detail untuk halaman destinasi',
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://images.unsplash.com/...',
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '2-3 jam',
            }),
            'difficulty': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mudah / Sedang / Sulit',
            }),
            'best_time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'April - Oktober (musim kemarau)',
            }),
            'features': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Fitur 1, Fitur 2, Fitur 3',
            }),
            'activities': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Berenang, Fotografi, Trekking ringan',
            }),
            'is_eco_friendly': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'name': 'Nama Destinasi',
            'slug': 'Slug (URL)',
            'category': 'Kategori',
            'location': 'Lokasi',
            'short_description': 'Deskripsi Singkat',
            'description': 'Deskripsi Lengkap',
            'image_url': 'URL Foto',
            'duration': 'Durasi',
            'difficulty': 'Tingkat Kesulitan',
            'best_time': 'Waktu Terbaik Berkunjung',
            'features': 'Fitur (pisahkan dengan koma)',
            'activities': 'Aktivitas (pisahkan dengan koma)',
            'is_eco_friendly': 'Destinasi Ramah Lingkungan',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['description'].required = False
        self.fields['image_url'].required = False


class DestinationCategoryForm(forms.ModelForm):
    class Meta:
        model = DestinationCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama kategori',
            }),
        }
        labels = {
            'name': 'Nama Kategori',
        }
