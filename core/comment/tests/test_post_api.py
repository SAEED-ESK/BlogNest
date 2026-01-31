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
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.mark.django_db
class TestPostAPI:

    def test_anonymouse_user_cannot_create_comment(self, api_client, post):
        '''
        Anonymouse user can NOT create comment
        '''
        url = reverse(
            "comment:api-v1:post-comments", kwargs={'post_id': post.id}
        )
        response = api_client.post(url, {'body': 'test anonymouse'})
        assert response.status_code == 401

    def test_authenticated_user_can_create_comment(self, auth_client, post, user):
        '''
        Authenticated user CAN create comment
        '''
        url = reverse(
            "comment:api-v1:post-comments", kwargs={'post_id': post.id}
        )
        response = auth_client.post(url, {'body': 'test authenticated'})
        assert response.status_code == 201
        assert response.data['body'] == 'test authenticated'

    def test_comment_user_is_logged_in_user(self, auth_client, post, user):
        '''
        Created comment belongs to logged in user
        '''
        url = reverse(
            "comment:api-v1:post-comments", kwargs={'post_id': post.id}
        )
        response = auth_client.post(url, {'body': 'test authenticated'})
        comment = Comment.objects.first()
        assert comment.author == user

    def test_create_comment_with_empty_body_is_invalid(self, auth_client, post, user):
        '''
        Create comment with empty body is invalid
        '''
        url = reverse(
            "comment:api-v1:post-comments", kwargs={'post_id': post.id}
        )
        response = auth_client.post(url, {'body': ''})
        assert response.status_code == 400
