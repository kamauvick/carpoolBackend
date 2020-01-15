from django.conf import settings
from django.conf.urls.static import static

from django.urls import re_path, include
from . import views
# FCM NOTIFICATIONS
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

# Switch to FCMDeviceViewSet when authentication is not nedeed
router = DefaultRouter()
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import (
    ProfileView ,
    RequestBoardViewSet,
    TripDetailApiView,
    TripApiView,
    TripChatApiView,
    DemandViewSet,
    OffersList,
    get_otp,
    get_token,
    get_jwt_token,
    test_view
)

#Documentation
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = SimpleRouter()
router.register('profile', ProfileView)
router.register(r'request_board', RequestBoardViewSet)
router.register('trip_detail', TripDetailApiView)
router.register('trip', TripApiView)
router.register(r'devices', FCMDeviceAuthorizedViewSet)
router.register('chat',TripChatApiView)
router.register('offers', OffersList)
router.register('demand',DemandViewSet)

urlpatterns = [
    re_path(r'^register/', views.UserDataView.as_view()),
    re_path(r'^auth/', include('rest_auth.urls')),
    re_path(r'^', include(router.urls)),
    re_path(r'^auth2/otp',get_otp),
    re_path(r'^auth2/jwt/token$', get_jwt_token),
    re_path(r'^auth2/jwt/token$', get_jwt_token),
    re_path(r'^auth2/token', get_token),
    re_path(r'^auth2/test', test_view),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
