from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    phone_number = models.CharField(max_length=100,null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, default='sample.jpg',null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance,first_name=instance.username)

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
    PENDING=' PE '
    ACCEPTED=' AC '
    DENIDE=' DE '
    REQUEST_STATUS=[
    (PENDING,"Pending"),
    (ACCEPTED,"Accepted"),
    (DENIDE,"Denied"),
    ]
    offer = models.ForeignKey(Offer, related_name='requests', on_delete=models.CASCADE)
    status = models.CharField(choices=REQUEST_STATUS,max_length=2)
    demand = models.ForeignKey(Demand, related_name='my_request', on_delete=models.CASCADE)

    class Meta:
        db_table="board_request"

    def __str__(self):
        return f'{self.demand.passanger.user.username} request to {self.offer.driver.user.username}'

class TripDetail(models.Model):
    request = models.ForeignKey(RequestBoard,on_delete=models.PROTECT)
    offer = models.ForeignKey(Offer ,on_delete=models.PROTECT)
    demand = models.ForeignKey(Demand ,on_delete=models.PROTECT)

    class Meta:
        db_table='trip_details'
        ordering =['offer']

    def __str__(self):
        return f"{self.offer.driver.user.username}'s trip to {self.offer.destination.name}"

class Trip(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT)
    start_time = models.TimeField()
    stop_time = models.TimeField()

    class Meta:
        db_table ="trip"
        ordering=['offer']

    def __str__(self):
        return f'trip to {self.offer.destination}'

class TripChat(models.Model):
    user = models.ForeignKey(Profile, on_delete = models.PROTECT)
    message = models.TextField()
    offer = models.ForeignKey(Offer , on_delete = models.PROTECT)
    time =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{user.username} message'
