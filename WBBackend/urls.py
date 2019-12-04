from django.urls import path,re_path,include
from . import views

#FCM NOTIFICATIONS
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet,FCMDeviceViewSet
from rest_framework.routers import DefaultRouter

# Switch to FCMDeviceAuthorizedViewSet when authentication is ready
router = DefaultRouter()
router.register(r'devices', FCMDeviceViewSet)

urlpatterns = [
    path('main/' ,views.home, name='home'),
    path('offers/', views.OffersList.as_view()),
    re_path(r'^', include(router.urls))
]
