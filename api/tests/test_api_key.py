import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_api_key_success(api_client):

    url = reverse("create-api-key")
    response = api_client.post(url, {"email": "ed@gmail.com"}, format="json")

    assert response.status_code == 201
    assert "api_key" in response.data


@pytest.mark.django_db
def test_create_api_key_email_required(api_client):

    url = reverse("create-api-key")
    response = api_client.post(url, {"email": ""}, format="json")

    assert response.status_code == 400
    assert "This field may not be blank." in response.data["email"]


@pytest.mark.django_db
def test_create_api_key_email_invalid(api_client):

    url = reverse("create-api-key")
    response = api_client.post(url, {"email": "a"}, format="json")

    assert response.status_code == 400
    assert "Enter a valid email address." in response.data["email"]


@pytest.mark.django_db
def test_create_api_key_email_already_exists(api_client, user_exists):

    url = reverse("create-api-key")
    response = api_client.post(
        url, {"email": "edcarlos.molequedoido@gmail.com"}, format="json"
    )

    assert response.status_code == 400
    assert "Email ja cadastrado!" in response.data["email"]
