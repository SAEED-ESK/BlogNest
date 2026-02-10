from rest_framework.test import APIClient
from django.urls import reverse

from ..models import Category
from accounts.models import User
import pytest

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def user():
    user = User.objects.create_user(
        email='test@test.com',
        password='zZ@12345'
    )
    return user

@pytest.fixture
def first_category():
    return Category.objects.create(
        name='test'
    )

@pytest.fixture
def url(first_category):
    return reverse('blog:api-v2:category-detail', kwargs={'pk': first_category.id})


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.mark.django_db

class TestCategoryDetailAPI:

    def test_category_update_by_unathorized(self, api_client, url):
        data = {
            'name': 'edited test'
        }
        response = api_client.put(url, data)
        assert response.status_code == 401

    def test_category_update_by_owner(self, auth_client, url):
        data = {
            'name': 'edited test'
        }
        response = auth_client.put(url, data)
        assert response.status_code == 200

    def test_category_create_with_invalid_data(self, auth_client, url):
        data = {
            'title': 'edited test',
        }
        response = auth_client.put(url, data)
        assert response.status_code == 400

    def test_delete_category_authorized(self, auth_client, url):
        response = auth_client.delete(url)
        assert response.status_code == 204
        assert Category.objects.count() == 0
        
    def test_anonymouse_user_cannot_delete_category(self, api_client, url):
        response = api_client.delete(url)
        assert response.status_code == 401
        