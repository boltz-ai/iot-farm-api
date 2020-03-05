# from django.urls import path
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=False)
router.register(r'sensors', views.SensorReadOnlyViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]
