from django.urls import path,re_path,include
from . import views

#FCM NOTIFICATIONS
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet,FCMDeviceViewSet
from rest_framework.routers import DefaultRouter

# Switch to FCMDeviceAuthorizedViewSet when authentication is ready
router = DefaultRouter()
router.register(r'devices', FCMDeviceViewSet)
router.register(r'request_board', views.RequestBoardViewSet) 
urlpatterns = [
    re_path(r'^', include(router.urls))
]
