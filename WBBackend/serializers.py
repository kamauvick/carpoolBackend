from rest_framework import serializers
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from .models import *
from rest_framework import status
import re
import requests

class ProfileSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise ValidationError(detail='The Profile cannot be created.')

    def update(self, instance, validated_data):
        if self.context['request'].user != instance.user:
            raise ValidationError(detail='You must be a user to edit.')
        phone_number = validated_data.get('phone_number', None)
        print(f'***Updated phone_number: {phone_number} ***')
        if phone_number is None:
            if not self.partial:
                raise ValidationError(
                    detail='The Phone_number must be provided.')
            else:
                instance.phone_number = phone_number
                # instance.profile_pic = profile_pic
                instance.save()
        return instance
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number',
                  'profile_pic', 'user', ]
        read_only_fields = ['user',]

class UserDataSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return super().create(validated_data)
    class Meta:
        model = UserData
        fields = ['first_name','last_name', 'username', 'phone_number', 'email',]

class LocaionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude=("")

class OfferSerializer(serializers.ModelSerializer):
    # driver_id = serializers.IntegerField()
    origin = serializers.CharField(max_length=20)
    destination = serializers.CharField(max_length=20)
    available_seats = serializers.IntegerField()
    departure_time = serializers.TimeField()
    created_at = serializers.DateTimeField()
    is_full = serializers.BooleanField()
    is_ended = serializers.BooleanField()

    def create(self, validated_data):
        return Offer.objects.create(**validated_data)

    def update(self, instance, validated_data, many=True):
        instance.driver = validated_data.get('driver', instance.driver)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.available_seats = validated_data.get('available_seats', instance.available_seats)
        instance.departure_time = validated_data.get('depature_time', instance.departure_time)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.is_full = validated_data.get('is_full', instance.is_full)
        instance.is_ended = validated_data.get('is_ended', instance.is_ended)

        instance.save()
        return instance
    class Meta:
        model = Offer
        fields = ('driver','origin','destination','available_seats',
                'departure_time','created_at', 'is_full','is_ended')


class DemandSerializer(serializers.ModelSerializer):
    passenger = ProfileSerializer(read_only=True)
    origin = LocaionSerializer()
    destination = LocaionSerializer()
    class Meta:
        model = Demand
        fields = ('passenger','origin','destination','available_seats',
                'departure_time','created_at')


class RequestBoardSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        exist = RequestBoard.objects.filter(
            demand=validated_data['demand']).first()
        if exist:
            serializer = RequestBoardSerializer(exist)
            details = {"status": status.HTTP_400_BAD_REQUEST,
                       "message": "User already has an existing request.Cancel requet to make another",
                       "request_board": serializer.data}
            raise ValidationError(detail=details)
        return RequestBoard.objects.create(**validated_data)
    class Meta:
        model = RequestBoard
        exclude = ""



class TripDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripDetail
        exclude = ("")

class TripSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        raise MethodNotAllowed(status.HTTP_405_METHOD_NOT_ALLOWED,
                               detail="Post request is not allowed in this field")
    class Meta:
        model = Trip
        exclude = ("")


class TripChatSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_profile = validated_data.get('user')
        offer = validated_data.get('offer')
        trip_details = TripDetail.objects.filter(
            offer=offer, demand__passenger=user_profile).first()
        if trip_details:
            return TripChat.objects.create(**validated_data)
        raise ValidationError(
            detail="This user is not allowed to send message for he is not part of this trip")

    class Meta:
        model = TripChat
        exclude = ("")
