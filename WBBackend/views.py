from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet

from . import notification
from .models import Profile
from .serializers import ProfileSerializer


def home(request):
    user = User.objects.get(pk=1)
    notification.request_notifications(user, "Hey Vick", "This is a test")
    return JsonResponse({'user': user.username})


# Create your views here.

class ProfileView(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    # permission_classes = (IsAuthenticated)

    def get_queryset(self):
        profile = self.request.user.profile
        if self.action in ['list', 'retrieve']:
            return [profile]

    def get_object(self):
        return self.request.user.profile
