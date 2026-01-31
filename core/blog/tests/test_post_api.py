from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime
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
class TestPostAPI:
    client = APIClient()

    def test_get_post_response_status_200(self, api_client):
        url = reverse('blog:api-v2:post-list')
        response = api_client.get(url)
        assert response.status_code == 200

    def test_post_create_response_status_401(self, api_client):
        url = reverse('blog:api-v2:post-list')
        data = {
            'title': 'test',
            'content': 'test desc',
            'status': True,
            'published_date': datetime.now()
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_post_create_response_status_201(self, api_client, commen_user):
        url = reverse('blog:api-v2:post-list')
        data = {
            'title': 'test',
            'content': 'test desc',
            'status': True,
            'published_date': datetime.now()
        }
        api_client.force_authenticate(user=commen_user)
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_post_create_invalid_data_response_status_400(self, api_client, commen_user):
        url = reverse('blog:api-v2:post-list')
        data = {
            'title': 'test',
        }
        api_client.force_authenticate(user=commen_user)
        response = api_client.post(url, data)
        assert response.status_code == 400