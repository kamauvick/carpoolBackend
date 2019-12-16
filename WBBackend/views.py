from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from .models import *
from . import notification
from .serializers import *
from rest_framework.exceptions import ValidationError,MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# Create your views here.
from .serializers import ProfileSerializer
from WBBackend.validate_user import ValidateUser
from WBBackend.create_user import create_new_user

class UserDataView(APIView):
    def get(self, request, format=None):
        dummy_param = 'dummy'
        email = self.request.query_params.get('email')
        api_key = self.request.query_params.get('apiKey')
        
        # Validate passed user emails 
        try:
            valid_email = ValidateUser.validate_email(dummy_param,email)
            print(valid_email)
            try:
                #Check if a user exists and get user data
                my_user = ValidateUser.check_if_user_exists(
                                                            dummy_param,
                                                            api_key,
                                                            valid_email
                                                            )
                print(my_user)
                print(my_user['name'])
                
                #Call create_new_user function
                create_new_user(
                                dummy_param, 
                                my_user['id'], 
                                my_user['name'].split()[0],
                                my_user['name'].split()[1],
                                my_user['username'], 
                                my_user['name'].split()[0], 
                                my_user['email'], 
                                my_user['phone_number']
                                )
            except Exception as e:
                print(f'message : {e}')
        except Exception as e:
            print(f'message: {e}')
        users = UserData.objects.all()
        print(users)
        serializers = UserDataSerializer(users, many=True)
        return Response(serializers.data)
    
    

class ProfileView(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = self.request.user.profile
        if self.action in ['list', 'retrieve']:
            return [profile]

    def get_object(self):
        return self.request.user.profile

class OffersList(APIView):
    def get(self, request, format=None):
        all_offers = Offer.objects.all()
        serializers = OfferSerializer(all_offers, many=True)
        return Response([serializers.data])
    
    def post(self, request):
        offer = request.data.get('offer')
        serializer = OfferSerializer(data=offer)
        if serializer.is_valid(raise_exception=True):
            saved_offer = serializer.save()
        return Response({"Success": "Offer '{}' created succesfully".format(saved_offer.driver)})



class DemandsList(APIView):
    def get(self, request, format=None):
        all_demands = Demand.objects.all()
        serializers = DemandSerializer(all_demands, many=True)
        return Response(serializers.data)


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
        """
        This function is ment to allow creating of a request board
        """
        profile = request.user.profile
        return self.create(request, profile, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        This function allows drivers to update the request status
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        This function is ment to allow cancling a request by deleteing a request
        """
        return self.destroy(request, *args, **kwargs)


class TripDetailApiView(ModelViewSet):
    queryset = TripDetail.objects.all()
    serializer_class = TripDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print("*********** 1 ************")
        offer_id = self.request.query_params.get('offer')

        if offer_id:
            print("*********** 2 ************")
            offer_id = int(offer_id)
            return TripDetail.objects.filter(offer__id=offer_id).all()

    def retrive(self, request, *args, **kwargs):
        error_message = {"status": status.HTTP_400_BAD_REQUEST,
                         "error": "Please pass an offer id query param",
                         "example": "{'offer':ID}"}
        return Response(error_message, safe=False)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class TripApiView(ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        offer_id = self.request.query_params.get('offer')
        if offer_id:
            offer_id = int(offer_id)
            print("*********** 1 ************")
            return Trip.objects.filter(offer__id=offer_id).all()
        profile = self.request.user.profile
        return Trip.objects.filter(offer__driver=profile).all()

    def post(self, request, *args, **kwargs):
        raise MethodNotAllowed(status.HTTP_400_METHOD_NOT_ALLOWED,detail="Post request is not allowed in this field")
        # return create(self, *args, **kwargs)

class TripChatApiView(ModelViewSet):
    queryset = TripChat.objects.all()
    serializer_class = TripChatSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self,request,*args,**kwargs):
        print(request.user.profile)
        return []
    def post(self,request ,*args ,**kwargs):
        mtu = self.request.user.profile
        return self.create(request, mtu,*args,**kwargs)
