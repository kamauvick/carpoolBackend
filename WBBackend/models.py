from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, default='sample.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f'{self.first_name}'

    class Meta:
        db_table = 'users'


class Location(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    distance = models.IntegerField()


class Offer(models.Model):
    driver = models.ForeignKey('WBBackend.Profile', related_name='driver_profile', on_delete=models.PROTECT)
    origin = models.ForeignKey('WBBackend.Location', related_name='offer_origin', on_delete=models.PROTECT)
    destination = models.ForeignKey('WBBackend.Location', related_name='offer_destination', on_delete=models.PROTECT)
    available_seats = models.IntegerField()
    departure_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_full = models.BooleanField(default=False)
    is_ended = models.BooleanField(default=False)


class Demand(models.Model):
    passenger = models.ForeignKey('WBBackend.Profile', related_name='trip_passenger', on_delete=models.PROTECT)
    origin = models.ForeignKey('WBBackend.Location', related_name='demand_origin', on_delete=models.PROTECT)
    destination = models.ForeignKey('WBBackend.Location', related_name='demand_destination', on_delete=models.PROTECT)
    available_seats = models.IntegerField()
    departure_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class RequestBoard(models.Model):
    offer = models.ForeignKey(Offer, related_name='requests', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    demand = models.ForeignKey(Demand, related_name='my_request', on_delete=models.CASCADE)

    class Meta:
        db_table="board_request"

    def __str__(self):
        return f'{self.demand.passanger.user.username} request to {self.offer.driver.user.username}'

class TripDetails:
    request = models.ForeignKey(RequestBoard,on_delete=models.PROTECT)
    offer = models.ForeignKey(Offer ,on_delete=models.PROTECT)
    demand = models.ForeignKey(Demand ,on_delete=models.PROTECT)

    class Meta:
        db_name='trip_details'
        ordering =['offer']

    def __str__(self):
        return f"{self.offer.driver.user.username}'s trip to {self.offer.destination.name}"
