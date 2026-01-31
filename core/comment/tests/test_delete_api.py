from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime

from blog.models import Post
from accounts.models import User, Profile
from ..models import Comment
import pytest

@pytest.fixture
def api_client():
    return APIClient()

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
def post(user):
    profile = Profile.objects.get(user=user)
    return Post.objects.create(
        author=profile,
        title= 'test',
        content = 'desc',
        status = True,
        published_date = datetime.now()
    )

@pytest.fixture
def comment(user, post):
    return Comment.objects.create(
        post= post,
        author=user,
        body= 'good post!'
    )

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.mark.django_db
class TestDeleteAPI:

    def test_owner_can_delete_comment(self, auth_client, comment):
        '''
        Owner can delete comment
        '''
        url = reverse(
            "comment:api-v1:api-delete", kwargs={'pk': comment.id}
        )
        response = auth_client.delete(url)
        assert response.status_code == 204
        assert Comment.objects.count() == 0

    def test_non_owner_cannot_delete_comment(self, api_client, other_user, comment):
        '''
        Non Owner can NOT delete comment
        '''
        url = reverse(
            "comment:api-v1:api-delete", kwargs={'pk': comment.id}
        )
        api_client.force_authenticate(user=other_user)
        response = api_client.delete(url)
        assert response.status_code == 403
        
    def test_anonymouse_user_cannot_delete_comment(self, api_client, comment):
        '''
        Anonymouse user can NOT delete comment
        '''
        url = reverse(
            "comment:api-v1:api-delete", kwargs={'pk': comment.id}
        )
        response = api_client.delete(url)
        assert response.status_code == 401
        