from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from swelocaltoursapi.models import Tour, Location, User
from swelocaltoursapi.views.tour import TourSerializer


class TourTests(APITestCase):
    fixtures = ['users', 'locations', 'tours']

    def setUp(self):
        """Set up test dependencies."""
        self.user = User.objects.first()
        self.location = Location.objects.first()
        
        # self.location = Location.objects.first()
        # self.tour = Tour.objects.create(
        #     user_id=self.user,
        #     uid="testUid123",
        #     image="https://example.com/image.jpg",
        #     price=100.00,
        #     location=self.location,
        #     name="Sunset Safari",
        #     description="Enjoy a beautiful sunset tour",
        #     date="2025-06-15",
        #     time="18:00:00",
        #     duration=180,
        # )
        # self.url = "/tours/"

    def test_create_tour(self):
        """Test creating a new tour."""
        url = "/tours"
        
        tour = {
            "user_id": self.user.id,
            "uid": "testUid456",
            "image": "https://example.com/new-image.jpg",
            "price": 150.00,
            "location": self.location.id,
            "name": "Night Adventure",
            "description": "Explore the city at night",
            "date": "2025-07-10",
            "time": "21:00:00",
            "duration": 240
        }

        response = self.client.post(url, tour, format='json')

        new_tour = Tour.objects.last()
        
        expected =TourSerializer(new_tour).data
        
        self.assertEqual(expected, response.data)
        
   