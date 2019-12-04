from django.shortcuts import render
from django.http import JsonResponse

from . import notification
from django.contrib.auth.models import User
def home(request):
    user = User.objects.get(pk = 1)
    notification.request_notifications(user,"Hey Steve","This is a test")
    return JsonResponse({'user':user.username})
# Create your views here.
