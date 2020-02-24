from django.conf.urls import url
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_registration.api.views import (change_password, register, send_reset_password_link, reset_password,
                                         verify_registration)

from .views import LogoutView, ProfileView

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^register$', register, name='auth-register'),
    url(r'^verify-registration$', verify_registration, name='auth-verify-registration'),
    url(r'^send-reset-password-link$', send_reset_password_link, name='send-reset-password-link'),
    url(r'^reset-password$', reset_password, name='auth-reset-password'),
    url(r'^login$', TokenObtainPairView.as_view(), name='auth-login'),
    url(r'^refresh$', TokenRefreshView.as_view(), name='auth-refresh'),
    url(r'^logout$', LogoutView.as_view(), name='auth-logout'),
    # url(r'^/verify$', TokenVerifyView.as_view(), name='auth-verify'),
    url(r'^me$', ProfileView.as_view(), name='auth-profile'),
    url(r'^me/change-password$', change_password, name='auth-change-password'),
]
