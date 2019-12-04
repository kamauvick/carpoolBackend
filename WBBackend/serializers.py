from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *


class ProfileSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise ValidationError(detail='The Profile cannot be created.')

    def update(self, instance, validated_data):
        if self.context['request'].user != instance.user:
            raise ValidationError(detail='You must be a user to edit.')
        phone_number = validated_data.get('phone_number', None)
        # profile_pic = validated_data.get('profile_pic', None)
        print(phone_number)
        if phone_number is None:
            if not self.partial:
                raise ValidationError(detail='The Phone_number must be provided.')
            else:
                instance.phone_number = phone_number
                # instance.profile_pic = profile_pic
                instance.save()
            return instance

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'profile_pic', 'user', 'device_id', ]
        read_only_fields = ['user', 'device_id', ]



