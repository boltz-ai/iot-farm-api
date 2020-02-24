from datetime import timedelta
from unittest.mock import patch
from rest_framework import status
from django.urls import include, path, reverse
from rest_framework.test import URLPatternsTestCase
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.utils import aware_utcnow, datetime_to_epoch

from users.models import User
from .utils import APIViewTestCase


# Create your tests here.
class UserViewSetting(APIViewTestCase, URLPatternsTestCase):
    urlpatterns = [
        path(r'', include('authentication.urls')),
    ]
    fixtures = ['seeders.json']

    def setUp(self) -> None:
        self.login = 'admin1'
        self.password = 'Admin12345^'
        self.active_user = {
            User.USERNAME_FIELD: self.login,
            'password': self.password,
        }


class LoginViewTests(UserViewSetting):
    view_name = 'auth-login'

    def setUp(self) -> None:
        super().setUp()
        self.inactive_user = {
            User.USERNAME_FIELD: 'public',
            'password': 'public',
        }

    def test_login_success(self):
        """
        Ensure we can login successfully.
        """
        response = self.view_post(data=self.active_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_fields_missing(self):
        response = self.view_post(data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(User.USERNAME_FIELD, response.data)
        self.assertIn('password', response.data)

        response = self.view_post(data={User.USERNAME_FIELD: self.login})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

        response = self.view_post(data={'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(User.USERNAME_FIELD, response.data)

    def test_credentials_wrong(self):
        response = self.view_post(data={
            User.USERNAME_FIELD: self.login,
            'password': 'test_user',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_user_inactive(self):
        response = self.view_post(data=self.inactive_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)


class RefreshViewTests(UserViewSetting):
    view_name = 'auth-refresh'

    def setUp(self) -> None:
        super().setUp()

    def test_fields_missing(self):
        res = self.view_post(data={})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('refresh', res.data)

    def test_it_should_return_401_if_token_invalid(self):
        token = RefreshToken()
        del token['exp']

        res = self.view_post(data={'refresh': str(token)})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.data['code'], 'token_not_valid')

        token.set_exp(lifetime=-timedelta(seconds=1))

        res = self.view_post(data={'refresh': str(token)})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.data['code'], 'token_not_valid')

    def test_it_should_return_access_token_if_everything_ok(self):
        refresh = RefreshToken()
        refresh['test_claim'] = 'arst'

        # View returns 200
        now = aware_utcnow() - api_settings.ACCESS_TOKEN_LIFETIME / 2

        with patch('rest_framework_simplejwt.tokens.aware_utcnow') as fake_aware_utcnow:
            fake_aware_utcnow.return_value = now
            res = self.view_post(data={'refresh': str(refresh)})

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        access = AccessToken(res.data['access'])

        self.assertEqual(refresh['test_claim'], access['test_claim'])
        self.assertEqual(access['exp'], datetime_to_epoch(now + api_settings.ACCESS_TOKEN_LIFETIME))


class LogoutViewTests(UserViewSetting):
    view_name = 'auth-logout'

    def setUp(self) -> None:
        super().setUp()
        login_res = self.client.post(
            reverse(LoginViewTests.view_name),
            data=self.active_user,
        )
        self.token = login_res.data

    def test_logout_success(self):
        self.authenticate_with_token(api_settings.AUTH_HEADER_TYPES[0], self.token['access'])
        logout_res = self.view_post(data={'refresh': self.token['refresh']})

        self.assertEqual(logout_res.status_code, status.HTTP_200_OK)

    def test_fields_missing(self):
        self.authenticate_with_token(api_settings.AUTH_HEADER_TYPES[0], self.token['access'])
        res = self.view_post(data={})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('refresh', res.data)

    def test_no_access_token(self):
        res = self.view_post(data={'refresh': self.token['refresh']})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', res.data)
