from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes,permission_classes
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
from WBBackend.models import User
# Create your views here.
from .serializers import ProfileSerializer
from WBBackend.validate_user import ValidateUser
from WBBackend.create_user import create_new_user,generate_code
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import os
from .emails import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
import hashlib

@api_view(http_method_names=["POST", ])
@permission_classes([AllowAny, ])
def get_otp(request):
    email = request.data.get("email", None)
    if not email:
        return Response({"message": "must provide email"}, status=status.HTTP_400_BAD_REQUEST)
    u: User = User.objects.filter(email=email).first()
    if not u:
        return Response({"message": "User with those details does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    otp = str(int(os.urandom(2).hex(), base=16))[:6]
    u.otp = hashlib.sha512(otp.encode()).hexdigest()
    u.otp_used = False
    u.save()
    url = "<p> Pin is %s</P>" %otp
    send_mail("wpoolb@gmail.com", u.email,"Login Confirmation",url)
    return Response([])

@api_view(http_method_names=["POST",])
@permission_classes([AllowAny,])
def get_jwt_token(request):
    email = request.data.get("email", None)
    if not email:
        return Response({"message": "must provide email"}, status=status.HTTP_400_BAD_REQUEST)
    password = request.data.get("otp",None)
    if not password:
        return Response({"message": "must provide password"}, status=status.HTTP_400_BAD_REQUEST)
    u: User = User.objects.filter(email=email).first()
    if not u:
        return Response({"message": "Wrong email or password"}, status=status.HTTP_400_BAD_REQUEST)
    h = hashlib.sha512(password.encode()).hexdigest()
    if u.otp != h:
        return Response({"message": "Wrong email or password"}, status=status.HTTP_400_BAD_REQUEST)
    if u.otp_used:
        return Response({"message": "Used password try again"}, status=status.HTTP_400_BAD_REQUEST)
    t = RefreshToken.for_user(u)
    data = {}
    data["access_token"] = str(t.access_token)
    data["refresh_token"] = str(t)
    u.otp_used = True
    u.save()
    return Response(data)


@api_view(http_method_names=["POST", ])
@permission_classes([AllowAny, ])
def get_token(request):
    email = request.data.get("email", None)
    if not email:
        return Response({"message": "must provide email"}, status=status.HTTP_400_BAD_REQUEST)
    password = request.data.get("otp", None)
    if not password:
        return Response({"message": "must provide password"}, status=status.HTTP_400_BAD_REQUEST)
    u: User = User.objects.filter(email=email).first()
    if not u:
        return Response({"message": "Wrong email or password"}, status=status.HTTP_400_BAD_REQUEST)
    h = hashlib.sha512(password.encode()).hexdigest()
    if u.otp != h:
        return Response({"message": "Wrong email or password"}, status=status.HTTP_400_BAD_REQUEST)
    if u.otp_used:
        return Response({"message": "Used password try again"}, status=status.HTTP_400_BAD_REQUEST)
    t = Token.objects.filter(user=u).first()
    if not t:
        t = Token(user=u)
        t.key = t.generate_key()
        t.save()
    data = {}
    data["token"] = t.key
    u.otp_used = True
    u.save()
    return Response(data)

@api_view()
@permission_classes([IsAuthenticated,])
def test_view(request):
    return Response("hellow")

class UserDataView(APIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
    permission_classes_by_action = {'list': [AllowAny],}

    def get(self, request, format=None):
        email = self.request.query_params.get('email')
        api_key = self.request.query_params.get('apiKey')
        print(api_key)
        auth_code = generate_code()
        if email is None:
            raise ValidationError(detail='The email must be provided.' , code='400')
        if api_key is None:
            raise ValidationError(detail='The api_key must be provided.', code='400')
        if api_key is None and email is None:
            raise ValidationError(detail='The api_key and email must be provided.', code='400')
        else:
            # Validate passed user emails
            try:
                valid_email = ValidateUser.validate_email(email)
                print(f'***VALIDATED*** {valid_email} Successfully.')
                try:
                    #Check if a user exists and get user data
                    my_user = ValidateUser.check_if_user_exists(api_key, valid_email)
                    print(my_user)

                    if my_user is None:
                        raise 

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

class SurveyApiView(ModelViewSet):
    serializer_class = SurveySerializer
    permission_classes = [AllowAny]
    # queryset = Survey.objects.all()

    #Test data
    
    survey = [
        'How was the trip?', 
        'How was the overall trip experience?',
        'Would you use the app again?'
    ]


