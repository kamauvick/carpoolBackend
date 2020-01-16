from django.test import TestCase
from django.test import Client

from WBBackend.models import (
    UserData, 
    Profile,
    )

# Create your tests here.

# TODO: Learn how to use fixtures for testing

class TestUserData(TestCase):
    def setUp(self):
        new_user = UserData.objects.create(
            first_name = 'test',
            last_name = 'tester',
            username = 'test',
            phone_number = '0700000000',
            email = 'test@email.com'
        )

        # self.assertTrue(isinstance(new_user, self.UserData))

    def test_user_instance(self):
        pass
    
    def tearDown(self):
        pass


class TestProfile(TestCase):
    def setUp(self):
        pass

    def test_profile_instance(self):
        pass

    def test_profile_instance(self):
        pass

    def tearDown(self):
        pass

class TestLocation(TestCase):
    def setUp(self):
        pass

    def test_location_instance(self):
        pass
    
    def tearDown(self):
        pass


class TestOffer(TestCase):
    def setUp(self):
        pass
    
    def test_offer_instance(self):
        pass
    
    def tearDown(self):
        pass


class TestDemand(TestCase):
    def setUp(self):
        pass
    
    def test_demand_instance(self):
        pass
    
    def tearDown(self):
        pass


class TestRequestBoard(TestCase):
    def setUp(self):
        pass

    def test_request_board_instance(self):
        pass
    
    def tearDown(self):
        pass


class TestTripDetail(TestCase):
    def setUp(self):
        pass
    
    def test_trip_details_instance(self):
        pass
    
    def tearDown(self):
        pass


class TestTrip(TestCase):
    def setUp(self):
        pass

    def test_trip_instance(self):
        pass
    
    def tearDown(self):
        pass


class TestTripChat(TestCase):
    def setUp(self):
        pass
    
    def test_trip_chat_instance(self):
        pass
    
    def tearDown(self):
        pass


class TestSurver(TestCase):
    def setUp(self):
        pass
    
    def test_survey_instance(self):
        pass
    
    def tearDown(self):
        pass

class TestEmmisions(TestCase):
    def setUp(self):
        pass
    
    def test_emmisions_instance(self):
        pass
    
    def tearDown(self):
        pass


    


#Test Url endpoints

class TestRegisterEndpoint(TestCase):
    def setUp(self):
        client = Client()
        response = client.get('/user_auth/?apiKey=r9y7naiFAZ0E7EFsuV2GSeXhG8K8Yg3NquVvEsaI&email=waichigovick@gmail.com')

    def test_register_response(self):
        pass
    
    def tearDown(self):
        pass


class TestLoginEndpoint(TestCase):
    def setUp(self):
        client = Client()
        response = client.post('/login/', {'username':'vick', 'password': 'password'})
    
    def test_login_response(self):
        # self.assertEquals(self.response.status_code, 200)
        pass

    def tearDown(self):
        pass