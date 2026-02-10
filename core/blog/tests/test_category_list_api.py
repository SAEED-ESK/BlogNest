from rest_framework.test import APIClient
from django.urls import reverse

from accounts.models import User
import pytest

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def commen_user():
    user = User.objects.create_user(
        email='test@test.com',
        password='zZ@12345'
    )
    return user

@pytest.mark.django_db
class TestCategoryListAPI:
    client = APIClient()

    def test_get_category_response_status_200(self, api_client):
        url = reverse('blog:api-v2:category-list')
        response = api_client.get(url)
        assert response.status_code == 200

    def test_category_create_unauthorized(self, api_client):
        url = reverse('blog:api-v2:category-list')
        data = {
            'name': 'test'
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_category_create_authorized(self, api_client, commen_user):
        url = reverse('blog:api-v2:category-list')
        data = {
            'name': 'test'
        }
        api_client.force_authenticate(user=commen_user)
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_category_create_with_invalid_data(self, api_client, commen_user):
        url = reverse('blog:api-v2:category-list')
        data = {}
        api_client.force_authenticate(user=commen_user)
        response = api_client.post(url, data)
        assert response.status_code == 400
