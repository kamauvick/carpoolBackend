import requests 
import re


class ValidateUser():
    """
    A class to `Validate user data` and `obtain a user object`
    """
    #Validate Passed address Email
    def validate_email(self, email):
        """
        A function to `validate the user emails` passed by the user. It uses `regex` to validate whether
        the email is valid or not.
        
        """
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(regex,email):
            print('The email you provided is valid.')
        else:
            print('The email you provided is invalid.')

    
    # Check if user exists on the DB    
    def check_if_user_exists(self, api_key, email):
        """
        A function that get passed `query params` from the user request and `makes a get request
        to the user DB` to obtain a user object
        """
        url= f'http://bw0rld.herokuapp.com/wb_users/?apiKey={api_key}&email={email}'
        headers = {
            'authorization': "Token 46e32eb8c65cf1f0af7923cf2b821198ef6a8474",
            'content-type': "application/json"
        }
        response = requests.request("GET", url=url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code + 'The request failed')
         