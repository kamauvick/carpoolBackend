from django.urls import re_path, include

# FCM NOTIFICATIONS
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

# Switch to FCMDeviceViewSet when authentication is not nedeed
router = DefaultRouter()
from rest_framework.routers import SimpleRouter

from .views import (
    ProfileView ,
    RequestBoardViewSet,
    TripDetailApiView,
    TripApiView,
    TripChatApiView,

)

router = SimpleRouter()
router.register('profile', ProfileView)
router.register(r'request_board', RequestBoardViewSet)
router.register('trip_detail', TripDetailApiView)
router.register('trip', TripApiView)
router.register(r'devices', FCMDeviceAuthorizedViewSet)
router.register('chat',TripChatApiView)
urlpatterns = [
    re_path(r'^', include(router.urls)),
    # re_path(r'^accounts/', include('allauth.urls')),
    re_path(r'^auth/', include('rest_auth.urls')),
    re_path(r'^auth/register/', include('rest_auth.registration.urls')),
]
