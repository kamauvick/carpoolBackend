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
