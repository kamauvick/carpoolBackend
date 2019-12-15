import requests 
import re

class ValidateUser():
    #Validate Passed address Email

    def validate_email(self, email):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(regex,email):
            print('The email you provided is valid.')
            return email
        else:
            print('The email you provided was invalid.')

    
    # Check if user exists on the DB    
    def check_if_user_exists(self, api_key, email):
        my_user_object = []
        url= f'http://bw0rld.herokuapp.com/wb_users/?apiKey={api_key}&email={email}'
        print(url)
        headers = {
            'authorization': "Token 46e32eb8c65cf1f0af7923cf2b821198ef6a8474",
            'content-type': "application/json"
        }
        response = requests.request("GET", url=url, headers=headers)
        print(response.json())
        if response.status_code == 200:
            print(response.json())
        else:
            print('The request failed')
         