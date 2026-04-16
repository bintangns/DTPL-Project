from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'email', 'rating', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nama Anda'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@contoh.com'}),
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tulis ulasan Anda'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError('Rating harus antara 1 sampai 5.')
        return rating

class AdminReplyForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['admin_reply']
        widgets = {
            'admin_reply': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tulis balasan admin...'
            })
        }