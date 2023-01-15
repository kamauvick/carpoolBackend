from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = '+12166665403'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) #twilio account client

import datetime as dt
CAVEMANAGER = ("Desolation Wilderness", "Ranger Maria", 7038877463) #to be hard coded into device
##############################################
##############################################
# UPDATE: to be imported somehow from database
##############################################
##############################################
check_in = {"photo": "123.jpg", "date_time": dt.datetime(2020,3,7,10,0),
"user": (123456, "Sonia Meyer", 7038877463), "group_size": 3,
"expected_out": dt.datetime(2020,3,7,18,0), "call_out": dt.datetime(2020,3,8,8,0)}
check_out = {"photo": "456.jpg", "date_time": dt.datetime(2020,3,7,18,30),
"user": (123456, "Sonia Meyer", 7038877463), "group_size": 3}
missed_checkout = {"photo": "456.jpg", "date_time": dt.datetime(2020,3,7,23,00),
"user": (123456, "Sonia Meyer", 7038877463), "group_size": 3}
##############################################
##############################################

##############################################
##############################################
def check_user_status(user):
    '''the check_user_status function references the database and returns
    user status whether they are in or out of the cave'''
    if user == "in": return False
    if user == "out": return True
##############################################
##############################################

def checked_out():
    '''the checked_out will send user a confirmation message'''
    client.messages.create(
        to='+1'+str(check_in["user"][2]), #user phone number
        from_=TWILIO_PHONE_NUMBER,
        body='Thanks for visiting {}, you are checked out!'.format(CAVEMANAGER[0])
    )
    return

def missed_expected_out():
    '''the missed_expected_out will check user status at initiate_contact time,
    then check with user if they forgot to check out of cave'''
    if check_user_status("in"):
        return
    client.messages.create(
        to='+1'+str(check_in["user"][2]), #user phone number
        from_=TWILIO_PHONE_NUMBER,
        body='Thanks for visiting {}, did you exit with all {} people?'.format(CAVEMANAGER[0],check_in["group_size"])
    )
    return

def missed_call_out():
    '''the missed_call_out will check user status at call out time, then notify
    the cave manager to initiate rescue if user is not out'''
    if check_user_status("in"):
        return
    client.messages.create(
        to='+1'+str(CAVEMANAGER[2]), #manager phone number
        from_=TWILIO_PHONE_NUMBER,
        body='{}, {} was visiting {} and did not check out before their call out time of {}.'.format(CAVEMANAGER[1],check_in["user"][1],CAVEMANAGER[0],check_in["call_out"])
    )
    return
