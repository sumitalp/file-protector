# fixtures to be accessed globally across all tests can be put here
import random

from django.core.files.base import ContentFile
from factory.django import ImageField
import pytest
from rest_framework.test import APIClient

from file_protector.apps.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def enable_db_access(db):
    """
    Global DB access to all tests.
    :param db:
    :return:
    """
    pass


@pytest.fixture
def synchronize_celery_tasks(settings):
    """
    https://pytest-django.readthedocs.io/en/latest/helpers.html#settings
    :param settings:
    :return:
    """
    settings.CELERY_TASK_ALWAYS_EAGER = True


@pytest.fixture
def client():
    """
    better off using rest framework's api client instead of built in django test client for pytest
    since we'll be working with developing and testing apis
    :return:
    """
    return APIClient()


@pytest.fixture
def image():
    return ContentFile(
        ImageField()._make_data({"width": 1024, "height": 768}), "image.jpg"
    )


@pytest.fixture
def link_to_protect():
    return random.choice([
        "https://google.com",
        "https://webdevahsan.wordpress.com",
        "https://dev.to/ahsankhan",
        "https://yahoo.com"
    ])

@pytest.fixture
def user():
    return UserFactory(password="PASSWORD")


@pytest.fixture
def auth_client(user, client):
    client.force_authenticate(user)
    return client
