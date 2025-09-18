import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_news_search_status(api_client, api_key_exists):
    key = api_key_exists.api_key
    url = reverse("search_news") + f"?search=brasil&api_key={key}"
    response = api_client.get(url)
    assert response.status_code == 200
    assert isinstance(response.data, dict)
