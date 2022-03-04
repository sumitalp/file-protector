from factory import fuzzy
from django.urls import reverse_lazy
from .factories import UploaderFactory

class TestUploader:
    def test_add_file(self, auth_client, image):
        url = reverse_lazy("api:api-uploader:api-file-add")
        data = {
            "uploaded_file": image,
            "title": fuzzy.FuzzyText(length=20).fuzz()
        }
        response = auth_client.post(url, data)
        assert response.status_code == 201

    def test_list_image_files(self, client, image):
        uploader = UploaderFactory(uploaded_file=image)
        url = reverse_lazy("api:api-uploader:api-file-list")
        response = client.get(url)

        assert response.data.get("count") > 0
