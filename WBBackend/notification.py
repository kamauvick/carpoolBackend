from fcm_django.models import FCMDevice


def request_notifications(receiver, msg_title, msg_message):
    device = FCMDevice.objects.filter(user=receiver).first()
    pool_icon = "https://icon-library.net/images/carpool-icon/carpool-icon-0.jpg"
    notification = device.send_message(title=msg_title, body=msg_message, icon=pool_icon)
    print(notification)
