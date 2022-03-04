import logging
import random

from django import forms
from django.conf import settings

from .models import Uploader
from .utils import StringShortener

logger = logging.getLogger(__name__)


class UploaderAdminForm(forms.ModelForm):
    class Meta:
        model= Uploader
        fields=[
            'title',
           'uploaded_file',
           'uploaded_url',
           'generated_url',
           'password',
           'visited'
        ]
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True): 
        obj = super().save(commit=False)
        obj.generated_url = f"{settings.BASE_URL}/link/{StringShortener().encode_url(n=random.randint(10**10, 10**11 - 1))}/"
        obj.save()

        return obj


class UploaderForm(UploaderAdminForm):
    class Meta:
        model = Uploader
        fields=[
            'title',
           'uploaded_file',
           'uploaded_url',
        ]
        widgets = {
            'password': forms.PasswordInput()
        }
