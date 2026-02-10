from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime

from ..models import Post
from accounts.models import User, Profile
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
def other_user():
    user = User.objects.create_user(
        email='other@test.com',
        password='zZ@12345'
    )
    return user

@pytest.fixture
def first_post(user):
    profile = Profile.objects.get(user=user)
    return Post.objects.create(
        author=profile,
        title= 'test',
        content = 'desc',
        status = True,
        published_date = datetime.now()
    )

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.mark.django_db

class TestPostDetailAPI:

    def test_post_update_by_unathorized(self, api_client, first_post):
        url = reverse('blog:api-v2:post-detail', kwargs={'pk': first_post.id})
        data = {
            'title': 'test',
            'content': 'test desc',
            'status': True,
            'published_date': datetime.now()
        }
        response = api_client.put(url, data)
        assert response.status_code == 401

    def test_post_update_by_non_owner(self, api_client, other_user, first_post):
        url = reverse('blog:api-v2:post-detail', kwargs={'pk': first_post.id})
        data = {
            'title': 'test',
            'content': 'test desc',
            'status': True,
            'published_date': datetime.now()
        }
        api_client.force_authenticate(user=other_user)
        response = api_client.put(url, data)
        assert response.status_code == 403

    def test_post_update_by_owner(self, auth_client, first_post):
        url = reverse('blog:api-v2:post-detail', kwargs={'pk': first_post.id})
        data = {
            'title': 'test',
            'content': 'test desc',
            'status': True,
            'published_date': datetime.now()
        }
        response = auth_client.put(url, data)
        assert response.status_code == 200

    def test_post_create_with_invalid_data(self, auth_client, first_post):
        url = reverse('blog:api-v2:post-detail', kwargs={'pk': first_post.id})
        data = {
            'title': 'test',
        }
        response = auth_client.put(url, data)
        assert response.status_code == 400

    def test_owner_can_delete_post(self, auth_client, first_post):
        url = reverse('blog:api-v2:post-detail', kwargs={'pk': first_post.id})
        response = auth_client.delete(url)
        assert response.status_code == 204
        assert Post.objects.count() == 0

    def test_non_owner_cannot_delete_post(self, api_client, other_user, first_post):
        url = reverse('blog:api-v2:post-detail', kwargs={'pk': first_post.id})
        api_client.force_authenticate(user=other_user)
        response = api_client.delete(url)
        assert response.status_code == 403
        
    def test_anonymouse_user_cannot_delete_post(self, api_client, first_post):
        url = reverse('blog:api-v2:post-detail', kwargs={'pk': first_post.id})
        response = api_client.delete(url)
        assert response.status_code == 401
        