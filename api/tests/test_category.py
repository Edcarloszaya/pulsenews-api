import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_category_miss_api_key(api_client):
    key = ""
    url = reverse("category_news") + f"?category=geral&api_key={key}"
    response = api_client.get(url)
    assert response.status_code == 403
    assert "error" in response.data
    assert "API key obrigatoria" in response.data["error"]


@pytest.mark.django_db
def test_category_success(api_client, api_key_exists):
    key = api_key_exists.api_key
    url = reverse("category_news") + f"?category=geral&api_key={key}"
    response = api_client.get(url)
    assert response.status_code == 200
    assert "results" in response.data
    assert response.data["count"] >= 0


@pytest.mark.django_db
def test_category_invalid(api_client, api_key_exists):
    category = "'Invalid'"
    key = api_key_exists.api_key
    url = reverse("category_news") + f"?category={category}&api_key={key}"
    response = api_client.get(url)
    assert response.status_code == 400
    assert "error" in response.data
    assert f"não existe" in response.data["error"]
