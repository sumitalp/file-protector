import factory
from factory import fuzzy
from django.core.files.base import ContentFile
from django.utils import timezone

from file_protector.apps.uploader.models import Uploader

class UploaderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Uploader

    title = factory.Sequence(lambda n: "Title %03d" % n)

    uploaded_file = factory.LazyAttribute(
            lambda _: ContentFile(
                factory.django.ImageField()._make_data(
                    {'width': 1024, 'height': 768}
                ), 'example.jpg'
            )
        )

    created = fuzzy.FuzzyDateTime(timezone.now())