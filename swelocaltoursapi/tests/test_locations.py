from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from swelocaltoursapi.models import Location, User
from swelocaltoursapi.views.location import LocationSerializer


class LocationTests(APITestCase):
    fixtures = ['locations', 'users']

    def setUp(self):
        """Set up test dependencies."""
        self.user = User.objects.first()

    def test_create_location(self):
        """Test creating a new location."""
        url = "/locations"
        
        location = {
            "name": "Shelby Park",
            "address": "Shelby Ave & S 20th St, Nashville, TN 37206",
            "coordinates": {"latitude": 51.7756934, "longitude": 19.4659261},
            "uid": "KMnkWlm7NOSTfPj8D2GmPr2Kt232"
        }

        response = self.client.post(url, location, format='json')

        new_location = Location.objects.last()
        
        expected =LocationSerializer(new_location).data
        
        self.assertEqual(expected, response.data)
