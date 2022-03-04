from factory import Faker
from file_protector.apps.uploader.forms import UploaderForm

def test_uploader_form_with_file(image):
    form = UploaderForm({
        "uploaded_file": image,
        "title": f"{Faker('title')}"
    })

    assert not form.is_valid()

def test_uploader_form_with_url(link_to_protect):
    form = UploaderForm({
        "uploaded_url": link_to_protect,
        "title": f"{Faker('title')}"
    })

    assert form.is_valid()
