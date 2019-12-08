from rest_framework.viewsets import ModelViewSet

from .models import *
from .serializers import *
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from django.http import JsonResponse
from rest_framework.response import Response
# Create your views here.


class ProfileView(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_queryset(self):
        profile = self.request.user.profile
        if self.action in ['list', 'retrieve']:
            return [profile]

    def get_object(self):
        return self.request.user.profile


class RequestBoardViewSet(ModelViewSet):
    queryset = RequestBoard.objects.all()
    serializer_class = RequestBoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''
        This function is ment to allow query params search if no query params
        it returns all the available requests
        '''
        demand = self.request.query_params.get('demand')
        status = self.request.query_params.get('status')
        offer = self.request.query_params.get('offer')
        if status and demand:
            options = ["PE", "AC", "DE"]
            status = "PE" if 'p' in status.lower() else status
            status = "AC" if 'a' in status.lower() else status
            status = "DE" if 'd' in status.lower() else status
            if status not in options:
                raise ValidationError(detail={"error": "invalid stautus"})
            return RequestBoard.objects.filter(demand__pk=int(demand), status=status)
        if demand:
            return RequestBoard.objects.filter(demand__pk=int(demand))
        if offer:
            return RequestBoard.objects.filter(offer__pk=int(offer))
        return RequestBoard.objects.all()

    def post(self, request, *args, **kwargs):
        '''
        This function is ment to allow creating of a request board
        '''
        profile = request.user.profile
        return self.create(request, profile, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        '''
        This function allows drivers to update the request status
        '''
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        '''
        This function is ment to allow cancling a request by deleteing a request
        '''
        return self.destroy(request, *args, **kwargs)


class TripDetailApiView(ModelViewSet):
    queryset = TripDetail.objects.all()
    serializer_class = TripDetailsSerializer

    def get_queryset(self):
        print("*********** 1 ************")
        offer_id = self.request.query_params.get('offer')

        if offer_id:
            print("*********** 2 ************")
            offer_id = int(offer_id)
            return TripDetail.objects.filter(offer__id=offer_id).all()

    def retrive(self, request, *args, **kwargs):
        error_message = {"status": status.HTTP_400_BAD_REQUEST,
                         "error": "Please pass an offer id query param", "example": "{'offer':ID}"}
        return Response(error_message, safe=False)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TripApiView(ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_queryset(self):
        offer_id = self.request.query_params.get('offer')
        if offer_id:
            offer_id = int(offer_id)
            print("*********** 1 ************")
            return Trip.objects.filter(offer__id=offer_id).all()
        profile = self.request.user.profile
        return Trip.objects.filter(offer__driver=profile).all()
