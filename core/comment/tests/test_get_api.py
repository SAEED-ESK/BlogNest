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
def another_post(user):
    profile = Profile.objects.get(user=user)
    return Post.objects.create(
        author=profile,
        title= 'another test',
        content = 'another desc',
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
def another_comment(user, another_post):
    return Comment.objects.create(
        post= another_post,
        author=user,
        body= 'another good post!'
    )

@pytest.mark.django_db
class TestGetAPI:

    def test_get_comments_of_post(self, api_client, post, comment):
        '''
        Returns comments of that post
        '''
        url = reverse(
            "comment:api-v1:post-comments", kwargs={'post_id': post.id}
        )
        response = api_client.get(url)
        assert response.data['count'] == 1
        assert response.status_code == 200
        
    def test_get_comments_only_related_to_post(
            self, api_client, post, another_post, comment, another_comment
        ):
        '''
        does NOT returns comments of other posts
        '''
        url = reverse(
            "comment:api-v1:post-comments", kwargs={'post_id': post.id}
        )
        response = api_client.get(url)
        assert response.data['count'] == 1