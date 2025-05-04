from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["text"]
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Оставьте ваш отзыв...',
                'class': 'form-textarea'
            })
        }