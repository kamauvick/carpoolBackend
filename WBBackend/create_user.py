#Create new user
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
import random
import string
from WBBackend.emails import send_mail
from WBBackend.models import UserData


def create_new_user(self, id, first_name, last_name, username, password, email, phone_number):
    """
    Creates a new instance of User and a user authentication token
    """
    new_user = User.objects.create_user(username=username, password=password)
    userdata = UserData.objects.create(
        first_name=first_name, 
        last_name=last_name, 
        username=username, 
        phone_number=phone_number, 
        email=email
        )
    if new_user:
        new_user.save()
        userdata.save()
        # Generate user token
        token = Token.objects.create(user=new_user)
        print(f'Auth token: {token}')
        
        #Generate a unique 5 digit code 
        random_user_code = ''.join(random.sample(string.digits, 5))
        print(f'Confirmation code: {random_user_code}')
        
        #Send token to email
        sender = 'waichigovick@gmail.com'
        send_mail(sender=sender, receiver=email, subject=random_user_code, html=None)
        
    else:
        raise ValidationError(detail='The user object is empty') 
