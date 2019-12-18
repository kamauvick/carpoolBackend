from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
import random
import string
from WBBackend.emails import send_mail
from WBBackend.models import UserData

def generate_code():
    """Generate a unique random 5 digit code"""
    random_user_code = ''.join(random.sample(string.digits, 5))
    return random_user_code
        

#Create new user
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
        # Generate user authentication token
        token = Token.objects.create(user=new_user)
        print(f'Auth token: {token}')
        
        #Get a unique 5 digit code
        random_user_code  = generate_code()
        print(f'Confirmation code: {random_user_code}')
        
        #Send token to email
        sender = 'waichigovick@gmail.com'
        email_body= """
        <html>
            <head>
                <title> World Bank car pooling authentication </title>
            </head>
            <body>
                <h2> Hi %s </h2>
                <p>Your confirmation key is %s </p>
                
                <h5>Enjoy the pooling Experience </h5>
            </body>
        </html>
        
        """ %(username, random_user_code)
        send_mail(sender=sender, receiver=email, subject='Car Pooling App', html=email_body)
        
    else:
        raise ValidationError(detail='The user object is empty') 
