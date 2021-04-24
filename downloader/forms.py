from django import forms
from django.core import validators
from downloader.models import InstaProfiles

class InstaForm(forms.ModelForm):
    class Meta:
        model = InstaProfiles
        # fields = ('profile_name')
        exclude = ('created_at',)