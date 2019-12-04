from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from .models import *
from . import notification
@receiver(post_save, sender=RequestBoard)
def request_board(sender, instance,**kwargs):
    if instance.status == 'AL':
        passanger=instance.demand.passanger.user
        title = f"Request to {instance.offer.destination} accepted"
        message= f"{instance.offer.driver.first_name.capitalize()} has accepted your request to {instance.offer.destination}"
        notification.request_notifications(passanger,title,message)
    if instance.status == 'DE':
        passanger=instance.demand.passanger.user
        title = f"Request to {instance.offer.destination} declined"
        message= f"You request to {instance.offer.destination} has been declined by driver. Please select another offer"
        notification.request_notifications(passanger,title,message)
    if instance.status == 'PE':
        driver = instance.offer.driver.user
        title = f"Trip rerquest from {instance.demand.passanger.first_name.capitalize()}"
        message = f"Hey {instance.offer.driver.first_name.capitalize()}, {instance.demand.passanger.first_name.capitalize()} is requesting to go with you to {instance.offer.destination.location.name}"
        notification.request_notifications(driver,title,message)
