from django import forms
from django.utils.translation import gettext_lazy as _

from app_reviews.models import Review


class ReviewForm(forms.ModelForm):
    text = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-textarea',
                'placeholder': _('Текст отзыва')
            }
        )
    )
    
    class Meta:
        model = Review
        fields = ['text']
