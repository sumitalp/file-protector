from django.contrib import admin

from .forms import UploaderAdminForm
from .models import Uploader

@admin.register(Uploader)
class UploaderAdmin(admin.ModelAdmin):
    list_display = ["title", "uploaded_file", "uploaded_url", "generated_url", "visited"]
    # readonly_fields = ["generated_url",]
    form = UploaderAdminForm
