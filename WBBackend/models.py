from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserData(models.Model):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.username}'

    class Meta:
        db_table = 'userdata'
        verbose_name = 'userdata'
        verbose_name_plural = 'userdata'

class Profile(models.Model):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=100, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, default='sample.jpg', null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance, first_name=instance.username)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f'{self.first_name}'

    class Meta:
        db_table = 'profile'
        verbose_name = 'profile'
        verbose_name_plural = 'profile'
    

# TODO :Remove the distance field and add it to offer and demand models
class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'location'

class Offer(models.Model):
    driver = models.ForeignKey('WBBackend.Profile', related_name='driver_profile', on_delete=models.PROTECT)
    origin = models.ForeignKey('WBBackend.Location', related_name='offer_origin', on_delete=models.PROTECT)
    destination = models.ForeignKey('WBBackend.Location', related_name='offer_destination', on_delete=models.PROTECT)
    seats_needed = models.IntegerField()
    departure_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_full = models.BooleanField(default=False)
    is_ended = models.BooleanField(default=False)

    def __str__(self):
        return f'Offer by {self.driver} to {self.destination}'

    class Meta:
        db_table = 'offer'
        verbose_name = 'offer'
        verbose_name_plural = 'offers'

class Demand(models.Model):
    passenger = models.ForeignKey('WBBackend.Profile', related_name='trip_passenger', on_delete=models.PROTECT)
    origin = models.ForeignKey('WBBackend.Location', related_name='demand_origin', on_delete=models.PROTECT)
    destination = models.ForeignKey('WBBackend.Location', related_name='demand_destination', on_delete=models.PROTECT)
    available_seats = models.IntegerField()
    departure_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    distance = models.CharField(max_length=255)
    complete = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    def __str__(self):
        return f'Demand by {self.passenger} for {self.destination}'

    class Meta:
        db_table = 'demand'
        verbose_name = 'demand'
        verbose_name_plural = 'demands'

class RequestBoard(models.Model):
    PENDING = 'PE'
    ACCEPTED = 'AC'
    DENIDE = 'DE'
    REQUEST_STATUS = [
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (DENIDE, "Denied"),
    ]
    offer = models.ForeignKey(Offer, related_name='requests', on_delete=models.CASCADE)
    status = models.CharField(choices=REQUEST_STATUS, max_length=2)
    demand = models.ForeignKey(Demand, related_name='my_request', on_delete=models.CASCADE)

    class Meta:
        db_table = "board_request"

    def __str__(self):
        return f'{self.demand.passenger.user.username} request to {self.offer.driver.user.username}'

class TripDetail(models.Model):
    request = models.ForeignKey(RequestBoard, on_delete=models.PROTECT)
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT)
    demand = models.ForeignKey(Demand, on_delete=models.PROTECT)

    class Meta:
        db_table = 'trip_details'
        ordering = ['offer']

    def __str__(self):
        return f"{self.offer.driver.user.username}'s trip to {self.offer.destination.name}"

class Trip(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT)
    start_time = models.TimeField(null=True)
    stop_time = models.TimeField(null=True)

    class Meta:
        db_table = "trip"
        ordering = ['offer']

    def __str__(self):
        return f'trip to {self.offer.destination}'

class TripChat(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.PROTECT)
    message = models.TextField()
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.user.username}'s message"

    class Meta:
        db_table = 'tripchat'
        verbose_name = 'tripchat'
        verbose_name_plural = 'tripchat'

class Survey:
    user = models.ForeignKey(Profile, on_delete=models.PROTECT)
    question = models.CharField(max_length=20)
    response = models.CharField(max_length=20)

    def __str__(self):
        return f'This survey was submitted by {user.username}.'

    class Meta:
        db_table = 'survey'
        verbose_name = 'passenger_survey'
        verbose_name_plural = 'passenger_surveys'

class Emmissions:
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    saved_emmissions = models.FloatField()

    def __str__(self):
        return f'saved {saved_emmissions}"%" of carbon emmissions'

    class Meta:
        db_table = 'emmission'
        verbose_name = 'saved_carbon_emmission'
        verbose_name_plural = 'saved_carbon_emmisions'
