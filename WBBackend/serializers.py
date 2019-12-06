from .models import *
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import status

class RequestBoardSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        exsist = RequestBoard.objects.filter(
            demand=validated_data['demand']).first()
        if exsist:
            serializer = RequestBoardSerializer(exsist)
            details = {"status": status.HTTP_400_BAD_REQUEST,
                       "message": "User already has an exsisting request.Cancel requet to make another",
                       "request_board": serializer.data}
            raise ValidationError(detail=details)
        return RequestBoard.objects.create(**validated_data)

    class Meta:
        model = RequestBoard
        exclude = ("")
