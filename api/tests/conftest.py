import uuid

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from api.models import ApiKey


@pytest.fixture
def api_client():
    client = APIClient()

    yield client


@pytest.fixture
def user_exists():
    user = User.objects.create_user(
        username="edcarlos.molequedoido@gmail.com",
        email="edcarlos.molequedoido@gmail.com",
    )

    yield user

    user.delete()


@pytest.fixture
def api_key_exists():
    key = uuid.uuid4().hex
    # Corrigido para o campo correto do User
    user = User.objects.create(username="test", email="test@gmail.com")
    api_key = ApiKey.objects.create(user=user, api_key=key)
    yield api_key
