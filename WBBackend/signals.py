from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import *
from . import notification


def update_offer_details(instance):
    if instance.status == "AC":
        available_seats = instance.offer.seats_needed
        trip_details = TripDetail.objects.filter(offer=instance.offer).all().count()
        if int(available_seats) == int(trip_details):
            instance.is_full = True
            instance.save()

def get_passangers(instance):
    receivers = []
    trip_details= TripDetail.objects.filter(offer= instance.offer).all()
    for i in trip_details:
        receivers.append(i.demand.passenger.user)
    print(receivers)
    driver = instance.offer.driver.user
    if instance.user.user != driver:
        receivers.append(driver)
    if instance.user.user in receivers:
        receivers.remove(instance.user.user)
    return receivers

@receiver(post_save, sender=RequestBoard)
def request_board(sender, instance, **kwargs):
    if instance.status == 'AC':
        trip_details_exsist = TripDetail.objects.filter(
            request=instance, offer=instance.offer, demand=instance.demand).first()
        if trip_details_exsist == None:
            append_trip_details = TripDetail.objects.create(
                request=instance, offer=instance.offer, demand=instance.demand)
            if append_trip_details:
                print(append_trip_details)
            passenger = instance.demand.passenger.user
            title = f"Request to {instance.offer.destination.name.capitalize()} accepted"
            message = f"{instance.offer.driver.first_name.capitalize()} has accepted your request to {instance.offer.destination.name.capitalize()}"
            passenger = instance.demand.passenger.user
            title = f"Request to {instance.offer.destination.name.capitalize()} accepted"
            message = f"{instance.offer.driver.first_name.capitalize()} has accepted your request to {instance.offer.destination.name.capitalize()}"
            notification.request_notifications(passenger, title,
                                               message, instance)
            update_offer_details(instance)
    if instance.status == 'DE':
        trip_details_exsist = TripDetail.objects.filter(
            request=instance, offer=instance.offer, demand=instance.demand).first()
        if trip_details_exsist:
            trip_details_exsist.delete()
        passenger = instance.demand.passenger.user
        title = f"Request to {instance.offer.destination.name.capitalize()} declined"
        message = f"You request to {instance.offer.destination.name} has been declined by driver. Please select another offer"
        notification.request_notifications(passenger, title, message, instance)
    if instance.status == 'PE':
        trip_details_exsist = TripDetail.objects.filter(
            request=instance, offer=instance.offer, demand=instance.demand).first()
        if trip_details_exsist:
            trip_details_exsist.delete()
        driver = instance.offer.driver.user
        title = f"Trip rerquest from {instance.demand.passenger.first_name.capitalize()}"
        message = f"Hey {instance.offer.driver.first_name.capitalize()}, {instance.demand.passenger.first_name.capitalize()} is requesting to go with you to {instance.offer.destination.name}"
        notification.request_notifications(driver, title, message, instance)


@receiver(post_save, sender=Offer)
def update_trip(sender, created, instance, **kwargs):
    exsists = Trip.objects.filter(offer=instance).first()
    print('It exsist *********************')
    if exsists == None:
        print('We have created it *********************')
        Trip.objects.create(offer=instance)

@receiver(post_save,  sender = TripChat)
def notify_chat(sender, instance, **kwargs):
    receivers = get_passangers(instance)
    notification.chat_notification(receivers,f"Message From {instance.user.first_name.capitalize()}",instance.message.capitalize())
    print("**************",receivers)

@receiver(post_save, sender=Offer)
def end_demands(instance,**kwargs):
    if instance.is_ended:
        trip_details = TripDetail.objects.filter(offer = instance).all()
        if trip_details.exists():
            for detail in trip_details:
                demand = Demand.objects.filter(id = detail.demand.id ).first()
                demand.complete = True;
                demand.save()
