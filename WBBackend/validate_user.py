import requests
import re
from rest_framework.authtoken.models import Token
from decouple import config


class ValidateUser:
    """
    A class to `Validate user data` and `obtain a user object`
    """

    # Validate Passed Email address
    def validate_email(email):
        """
        A function to `validate the user emails` passed by the user. It uses `regex` to validate whether
        the email is valid or not.
        """
        regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"     
        if re.search(regex, email):
            print("The email you provided is valid.")
            return email
        else:
            print("The email you provided is invalid.")

    # Check if user exists on the DB
    def check_if_user_exists(api_key, email):
        """
        A function that get passed `query params` from the user request and `makes a get request
        to the user DB` to obtain a user object
        """
        url = f"http://bw0rld.herokuapp.com/wb_users/?apiKey={api_key}&email={email}"
        headers = {
            "Authorization": config('AUTHORIZATION'),
            "content-type": "application/json",
        }
        response = requests.request("GET", url=url, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code) 

    #Generate User auth tokens
    def generate_token(self, username, password):
        """
        A function to generate User authentication tokens
        """
        data = {"username": username, "password": password}
        token = Token.objects.create(user=data)
        return token

