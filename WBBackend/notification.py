from fcm_django.models import FCMDevice
from django.http import JsonResponse as JsonR
from rest_framework import status
from .serializers import RequestBoardSerializer

pool_icon = "https://icon-library.net/images/carpool-icon/carpool-icon-0.jpg"

def request_notifications(receiver, msg_title, msg_message,instance):
    serializer = RequestBoardSerializer(instance)
    notification_error= {"warning":"This user can not recieve notification because we lack the Device Id ","request":serializer.data}
    print("********** 0 **********")
    try:
        print("********** 1 **********")
        device = FCMDevice.objects.filter(user=receiver).first()
        notification = device.send_message(title=msg_title, body=msg_message, icon=pool_icon)
        print(notification)
    except Exception as e:
        print("********** 2 **********")
        return JsonR(notification_error,safe=False)

def chat_notification(receivers, msg_title, act_msg):
    for receiver in receivers:
        try:
            device = FCMDevice.objects.filter(user = receiver).first()
            device.send_message(title=msg_title, body=act_msg, icon=pool_icon)
            print('************************* worked')
        except Exception as e:
            print('************************* Failed Teribly')
            print(e)
