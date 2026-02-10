from rest_framework.test import APIClient
from django.urls import reverse
from django.core import mail
from unittest.mock import patch

from ..models import User
import pytest

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    user = User.objects.create_user(
        email='test@test.com',
        password='Zz12345#'
    )
    return user

@pytest.fixture
def auth_client_jwt(api_client, user):
    """
    A authenticated client with jwt token
    """
    url = reverse('accounts:api-v1:jwt-create')
    data = {
        'email': 'test@test.com',
        'password': 'Zz12345#'
    }
    response = api_client.post(url, data=data)
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

@pytest.mark.django_db
class TestAuthebticationAPI:

    def test_register_success(self, api_client):
        url = reverse('accounts:api-v1:registration')
        data = {
            "email": "test@test.com",
            "password": "Zz12345#",
            "password1": "Zz12345#"
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 201
        assert response.data['email'] == "test@test.com"

    def test_login_success(self, api_client, user):
        url = reverse('accounts:api-v1:jwt-create')
        data = {
            'email': 'test@test.com',
            'password': 'Zz12345#'
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 200
        assert "access" in response.data

    def test_profile_unauthorized(self, api_client):
        url = reverse('accounts:api-v1:profile')
        response = api_client.get(url)
        assert response.status_code == 401

    def test_profile_authorized(self, auth_client_jwt):
        url = reverse('accounts:api-v1:profile')
        response = auth_client_jwt.get(url)
        assert response.status_code == 200
        
    def test_change_password_unauthorized(self, api_client):
        url = reverse('accounts:api-v1:change-password')
        response = api_client.put(url)
        assert response.status_code == 401

    def test_change_password_wrong_old_password(self, auth_client_jwt):
        url = reverse('accounts:api-v1:change-password')
        data = {
            "old_password": "wrong",
            "new_password": "Zz12345@",
            "new_password1": "Zz12345@"
        }
        response = auth_client_jwt.put(url, data=data)
        assert response.status_code == 400

    def test_change_password_success(self, auth_client_jwt):
        url = reverse('accounts:api-v1:change-password')
        data = {
            "old_password": "Zz12345#",
            "new_password": "New12345#",
            "new_password1": "New12345#"
        }
        response = auth_client_jwt.put(url, data=data)
        assert response.status_code == 200

    def test_reset_password_send_email(self, api_client, user,):
        with patch('accounts.api.v1.utils.EmailThread.start') as mock_start:
            url = reverse('accounts:api-v1:reset-password-email')
            data = {
                "email": user.email
            }
            response = api_client.post(url, data=data)
        assert response.status_code == 200
        mock_start.assert_called_once()
