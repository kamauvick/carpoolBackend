# from django.contrib.auth import authenticate
# from rest_framework.authtoken.models import Token

# class AuthenticateUser():
#     """A class to authenticate users and log them in"""
#     def login_user(self, username, password):
#         user = authenticate(username=username, password=password)
#         try:
#             if user is not None:
#                 print('User authenticated')
#                 token = Token.objects.create(user=user)
#                 print(f'Auth token: {token}')
#         except Exception as e:
#             print(f'Error message: {e}')



