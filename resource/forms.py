from django import forms
from .models import EducationalResource


class EducationalResourceForm(forms.ModelForm):
    class Meta:
        model = EducationalResource
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter resource title'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Enter the educational content here...'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }