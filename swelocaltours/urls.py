from django.contrib import admin  # Use Django's admin module
from django.urls import path, include
from rest_framework import routers
from swelocaltoursapi.views.auth import check_user, register_user  # Import functions directly
from swelocaltoursapi.views import LocationView

# Initialize router
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'locations', LocationView, 'location')

# Define URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  # Include router-generated URLs
    path('checkuser/', check_user, name='check_user'),  # Custom endpoint
    path('registeruser/', register_user, name='register_user'),  # Custom endpoint
]


