from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes
from rest_framework.viewsets import ModelViewSet
from .models import *
from . import notification
from .serializers import *
from rest_framework.exceptions import ValidationError,MethodNotAllowed, NotFound, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# Create your views here.
from .serializers import ProfileSerializer
from WBBackend.validate_user import ValidateUser
from WBBackend.create_user import create_new_user,generate_code
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class UserDataView(APIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
    permission_classes_by_action = {'list': [AllowAny],}

    def get(self, request, format=None):
        email = self.request.query_params.get('email')
        api_key = self.request.query_params.get('apiKey')
        print(api_key)
        auth_code = generate_code()

        # Validate passed user emails
        try:
            valid_email = ValidateUser.validate_email(email)
            print(f'***VALIDATED*** {valid_email} Successfully.')
            try:
                #Check if a user exists and get user data
                my_user = ValidateUser.check_if_user_exists(api_key, valid_email)
                print(my_user)

                #Call create_new_user function
                create_new_user(
                                my_user['id'],
                                my_user['name'].split()[0],
                                my_user['name'].split()[1],
                                my_user['username'],
                                auth_code,
                                my_user['email'],
                                my_user['phone_number']
                                )
            except Exception as e:
                print(f'message : {e}')
        except Exception as e:
            print(f'message: {e}')
        users = UserData.objects.filter(email=email)
        print(users)

        serialized_users = UserDataSerializer(users, many=True)
        return Response(serialized_users.data)

    def list(self, request, *args, **kwargs):
        return super(UserDataView, self).list(request, *args, **kwargs)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action['list']]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


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

class OffersList(ModelViewSet):
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OfferSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        profile = self.request.user.profile
        return queryset.filter(driver = profile)
    
    def post(self, request, profile, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DemandViewSet(ModelViewSet):
    queryset = Demand.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DemandSerializer

    def get_queryset(self):
        profile = self.request.user.profile
        id = self.request.query_params.get('id')
        if id:
            object = Demand.objects.filter(pk = int(id))
            if object.exists():
                return object
            raise NotFound(detail="Demand with that ID does not exists")
        return Demand.objects.filter(passenger = profile)

    def post(self, request,profile, *args, **kwargs):
        return self.create(request, *args, **kwargs)

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
