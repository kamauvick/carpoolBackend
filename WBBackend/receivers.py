from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from .models import *
from . import notification
@receiver(post_save, sender=RequestBoard)
def request_board(sender, instance,**kwargs):
    if instance.status == 'AC':
        passenger=instance.demand.passenger.user
        title = f"Request to {instance.offer.destination.name.capitalize()} accepted"
        message= f"{instance.offer.driver.first_name.capitalize()} has accepted your request to {instance.offer.destination.name.capitalize()}"
        notification.request_notifications(passenger,title,message)
    if instance.status == 'DE':
        passenger=instance.demand.passenger.user
        title = f"Request to {instance.offer.destination.name.capitalize()} declined"
        message= f"You request to {instance.offer.destination.name} has been declined by driver. Please select another offer"
        notification.request_notifications(passenger,title,message)
    if instance.status == 'PE':
        driver = instance.offer.driver.user
        title = f"Trip rerquest from {instance.demand.passenger.first_name.capitalize()}"
        message = f"Hey {instance.offer.driver.first_name.capitalize()}, {instance.demand.passenger.first_name.capitalize()} is requesting to go with you to {instance.offer.destination.name}"
        notification.request_notifications(driver,title,message)
