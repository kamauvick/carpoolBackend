from .models import *
from rest_framework import serializers

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('driver','origin','destination','available_seats',
                'departure_time','created_at', 'is_full','is_ended')


class DemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demand
        fields = ('passenger','origin','destination','available_seats',
                'departure_time','created_at')
