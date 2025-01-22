from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from swelocaltoursapi import admin
from swelocaltoursapi.views import auth

router = routers.DefaultRouter(trailing_slash=False)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('checkuser', auth.check_user),  # Add the checkuser route here
    path('registeruser', auth.register_user),
  ]






