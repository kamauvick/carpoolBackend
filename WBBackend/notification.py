from fcm_django.models import FCMDevice
from django.http import JsonResponse as JsonR
from rest_framework import status
from .serializers import RequestBoardSerializer

def request_notifications(receiver, msg_title, msg_message,instance):
    serializer = RequestBoardSerializer(instance)
    notification_error= {"warning":"This user can not recieve notification because we lack the Device Id ","request":serializer.data}
    try:
        device = FCMDevice.objects.filter(user=receiver).first()
        pool_icon = "https://icon-library.net/images/carpool-icon/carpool-icon-0.jpg"
        notification = device.send_message(title=msg_title, body=msg_message, icon=pool_icon)
        print(notification)
    except Exception as e:
        return JsonR(notification_error,safe=False)
