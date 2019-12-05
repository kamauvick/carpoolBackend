from .models import *
from rest_framework import serializers

class OfferSerializer(serializers.ModelSerializer):
    driver_id = serializers.IntegerField()
    origin = serializers.CharField(max_length=20)
    destination = serializers.CharField(max_length=20)
    available_seats = serializers.IntegerField()
    departure_time = serializers.TimeField()
    created_at = serializers.DateTimeField()
    is_full = serializers.BooleanField()
    is_ended = serializers.BooleanField()

    def create(self, validated_data):
        return Offer.objects.create(**validated_data)

    def update(self, instance, validated_data):
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

    # class Meta:
    #     model = Offer
    #     fields = ('driver','origin','destination','available_seats',
    #             'departure_time','created_at', 'is_full','is_ended')


class DemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demand
        fields = ('passenger','origin','destination','available_seats',
                'departure_time','created_at')
