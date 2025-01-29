from django.contrib import admin  # Use Django's admin module
from django.urls import path, include
from rest_framework import routers
from swelocaltoursapi.views.auth import check_user, register_user  # Import functions directly
from swelocaltoursapi.views import LocationView, ItineraryView, TourView, UserView

# Initialize router
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'locations', LocationView, 'location')
router.register(r'itineraries', ItineraryView, 'itinerary')
router.register(r'tours', TourView, 'tour')
router.register(r'users', UserView, 'user')

# Define URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  # Include router-generated URLs
    path('checkuser/', check_user, name='check_user'),  # Custom endpoint
    path('registeruser/', register_user, name='register_user'),  # Custom endpoint
]
