from rest_framework import serializers
from rest_framework.exceptions import ValidationError, MethodNotAllowed, NotAcceptable, JsonResponse
from .models import *
from rest_framework import status
import re
import requests
import datetime
from django.db.models import Q


class ProfileSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise ValidationError(detail='The Profile cannot be created.')

    def update(self, instance, validated_data, many=True):
        if self.context['request'].user != instance.user:
            raise ValidationError(detail='You must be a user to edit.')
        phone_number = validated_data.get('phone_number')
        last_name = validated_data.get('last_name')
        profile_pic = validated_data.get('profile_pic')
        print(f'***phone_number: {phone_number} ***')
        if phone_number is None:
            raise ValidationError(
                detail='The Phone_number must be provided.')
        else:
            instance.phone_number = phone_number
            instance.last_name = last_name
            # instance.profile_pic= profile_pic
            # TODO: Fix profile_pic upload
            instance.save()
        return instance

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number',
                  'profile_pic', 'user', ]
        read_only_fields = ['user', ]


class UserDataSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = UserData
        fields = ['first_name', 'last_name',
                  'username', 'phone_number', 'email', ]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ("")


class OfferSerializer(serializers.ModelSerializer):
    origin = serializers.JSONField(required = True)
    destination = serializers.JSONField(required = True)
    seats_needed = serializers.IntegerField()
    departure_time = serializers.TimeField()
    is_full = serializers.BooleanField()
    is_ended = serializers.BooleanField()   

    driver = ProfileSerializer(read_only=True)
    origin = LocationSerializer()
    destination = LocationSerializer()

    def create(self, validated_data):
        now = datetime.datetime.now()
        depature_time = validated_data.get('departure_time')
        is_full = validated_data.get("is_full")  
        is_ended = validated_data.get("is_ended")
        request = self.context['request']
        try:
            validated_data['driver'] = request.user.profile
        except Exception as e:
            raise ValidationError(detail='User has no profile', code='001--no_profile')

        for item in ['origin','destination']:
            _location = Location.objects.create(**validated_data.get(item))
            validated_data[item] = _location
        return Offer.objects.create(**validated_data)

    def update(self, instance, validated_data, many=True):
      
        instance.is_full = validated_data.get('is_full', instance.is_full)
        instance.is_ended = validated_data.get('is_ended', instance.is_ended)       

        # TODO : Check bugs on this endpoint

        instance.save()
        return instance
        
    class Meta:
        model = Offer
        fields = ('driver','origin','destination','seats_needed',
                'departure_time','created_at', 'is_full','is_ended')



class DemandSerializer(serializers.ModelSerializer):
    departure_time = serializers.DateTimeField(required=True)
    origin = serializers.JSONField(required=True)
    destination = serializers.JSONField(required=True)
    distance = serializers.CharField(required=True)

    passenger = ProfileSerializer(read_only=True)
    origin = LocationSerializer()
    destination = LocationSerializer()

    def create(self, validated_data):
        request = self.context['request']
        if request and hasattr(request, "user"):
            try:
                validated_data['passenger'] = request.user.profile
                existing_demand = Demand.objects.filter(
                    Q(passenger=validated_data['passenger']), Q(complete=False) & Q(canceled=False))
                if existing_demand.exists():
                    existing_demand = existing_demand.first()
                    raise NotAcceptable(
                        detail=f"User already has an active demand of id {existing_demand.id}")
                    # raise NotAcceptable(detail="errors")
            except Exception as e:
                print(f"********* {e} *********")
                if int(str(e)[-1]):
                    raise NotAcceptable(
                        detail=f"User already has an active demand of id {existing_demand.id}")
                raise ValidationError(
                    detail="User has no Profile", code="invalid")
            data = request.data
            now = datetime.datetime.now()
            depature_year = validated_data['departure_time'].year

            depature_date = validated_data['departure_time'].date()
            depature_time = validated_data['departure_time'].time()
            final_date_time = datetime.datetime.combine(
                depature_date, depature_time)

            if final_date_time < now:
                raise NotAcceptable(
                    detail="You can not book a ride for the previous dates")
            if int(depature_year) > int(now.year) + 1:
                raise NotAcceptable(
                    detail=f"Chose a near year. {depature_year} is too far")

            for item in ['origin', 'destination']:
                a_location = Location.objects.create(
                    **validated_data.get(item))
                validated_data[item] = a_location
            return Demand.objects.create(**validated_data)
            # return Demand.objects.create(**validated_data)
        raise ValidationError(
            detail="You must be a user to create a demand", code="invalid")

    class Meta:
        model = Demand
        fields = ('id', 'passenger', 'origin', 'destination', 'available_seats',
                  'departure_time', 'created_at', 'distance', 'complete', 'canceled')


class RequestBoardSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        offer = validated_data['offer']
        print('i am starting *********************')
        if offer.is_full:
            print('It exsist *********************')
            raise ValidationError(detail="this offer is full")
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
