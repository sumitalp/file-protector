from django.db.models import CASCADE
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from .utils import file_path


class Uploader(TimeStampedModel):
    title = models.CharField(max_length=128)
    uploaded_file = models.FileField(blank=True, upload_to=file_path,)
    uploaded_url = models.URLField(blank=True)
    generated_url = models.URLField(blank=True)
    password = models.CharField(_('password'), max_length=128)
    visited = models.PositiveBigIntegerField(default=0)
    correct_pass_counter = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ('-created',)

    def clean(self):
        super().clean()
        error_dict = {}
        if not self.uploaded_file and not self.uploaded_url:
            error_dict["uploaded_file"] = ValidationError("Both file or url can't be null.")
            error_dict["uploaded_url"] = ValidationError("Both file or url can't be null.")

        if self.uploaded_file and self.uploaded_url:
            error_dict["uploaded_file"] = ValidationError("Both file and url can't be uploaded together.")
            error_dict["uploaded_url"] = ValidationError("Both file and url can't be uploaded together.")

        if error_dict:
            raise ValidationError(error_dict)

    def __str__(self) -> str:
        return self.title


class VisitorHistory(TimeStampedModel):
    uploader = models.ForeignKey(Uploader, related_name="visitors", on_delete=CASCADE)
    agent = models.TextField()

    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.uploader.title
