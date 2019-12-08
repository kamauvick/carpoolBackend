from django.urls import re_path, include

# FCM NOTIFICATIONS
from fcm_django.api.rest_framework import FCMDeviceViewSet
from rest_framework.routers import DefaultRouter

# Switch to FCMDeviceAuthorizedViewSet when authentication is ready
router = DefaultRouter()
router.register(r'devices', FCMDeviceViewSet)
from rest_framework.routers import SimpleRouter

from .views import (
    ProfileView ,
    RequestBoardViewSet,
    TripDetailApiView,
)

router = SimpleRouter()
router.register('profile', ProfileView)
router.register(r'request_board', RequestBoardViewSet)
router.register('trip_detail', TripDetailApiView)
urlpatterns = [
    # path('main/' ,views.home, name='home'),
    re_path(r'^', include(router.urls)),
    re_path(r'^accounts/', include('allauth.urls')),
    re_path(r'^auth/', include('rest_auth.urls')),
    re_path(r'^auth/register/', include('rest_auth.registration.urls')),
]
