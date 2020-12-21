from django import forms
from .models import Center


class CenterForm(forms.Form):
    name = forms.TextInput(attrs=None)
    location = forms.TextInput(attrs=None)
    logo = forms.FileInput(attrs=None)

    class Meta:
        model = Center
        fields = ['name', 'location', 'logo']
