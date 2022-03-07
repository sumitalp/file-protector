import random
from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from password_generator import PasswordGenerator

from file_protector.apps.uploader.models import Uploader, VisitorHistory
from file_protector.apps.uploader.utils import StringShortener


class UploaderSerializer(ModelSerializer):
    class Meta:
        model = Uploader
        fields = ["id", "uploaded_file", "uploaded_url", "title", "password", "generated_url"]
        read_only_fields = ("id", "password", "generated_url")

    def create(self, validated_data):
        copy_data = validated_data.copy()
        copy_data["password"] = PasswordGenerator().generate()
        copy_data["generated_url"] = f"{settings.BASE_URL}/link/{StringShortener().encode_url(n=random.randint(10**10, 10**11 - 1))}/"
        return super().create(copy_data)


class PasswordSerializer(ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Must provided to see this file or url.',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = Uploader
        fields = ["password"]


class UploaderVisitorSerializer(ModelSerializer):
    class Meta:
        model = VisitorHistory
        fields = ['uploader']
