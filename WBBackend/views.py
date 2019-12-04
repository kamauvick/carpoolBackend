from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from . import notification
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    user = User.objects.get(pk = 1)
    notification.request_notifications(user,"Hey Steve","This is a test")
    return JsonResponse({'user':user.username})


class OffersList(APIView):
    def get(self, request, format=None):
        all_offers = Offer.objects.all()
        serializers = OfferSerializer(all_offers, many=True)
        return Response(serializers.data)


