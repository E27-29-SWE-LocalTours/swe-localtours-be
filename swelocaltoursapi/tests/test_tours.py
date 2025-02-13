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
        
# Test to create a New tour 
# run this command: python manage.py test swelocaltoursapi.tests.test_tours

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
        
        
# Test to get a single tour
# run this command: python manage.py test swelocaltoursapi.tests.test_tours

    def test_get_tours(self):
        """ Get Tour Test
        """
        tour =Tour.objects.first()
        
        url = f'/tours/{tour.id}'
        
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        expected = TourSerializer(tour)
        
        self.assertEqual(expected.data, response.data)
   
#    Test to list all the tours 
# run this command: python manage.py test swelocaltoursapi.tests.test_tours

    def test_list_tours(self):
        """Test list tours
        """
        url = '/tours'
        
        response = self.client.get(url)
        
        all_tours = Tour.objects.all()
        expected = TourSerializer(all_tours, many=True)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)
        
# Test to Update a tour 
# run this command: python manage.py test swelocaltoursapi.tests.test_tours

    def test_change_tour(self):
        """test update tour
        """
        tour = Tour.objects.first()
        
        url = f'/tours/{tour.id}'
        
        updated_tour = {
            "user": self.user.id,
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
        
        response = self.client.put(url, updated_tour, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Ensure update is successful

        # Refresh the tour object to reflect any changes in the database
        tour.refresh_from_db()

        # Assert that the updated values match
        self.assertEqual(updated_tour["name"], tour.name)
        self.assertEqual(updated_tour["description"], tour.description)
        self.assertEqual(updated_tour["price"], tour.price)
        self.assertEqual(updated_tour["image"], tour.image)
        self.assertEqual(updated_tour["date"], str(tour.date))  # Ensure date is stored correctly
        self.assertEqual(updated_tour["time"], str(tour.time))  # Ensure time is stored correctly
        self.assertEqual(updated_tour["duration"], tour.duration)
        self.assertEqual(updated_tour["location"], tour.location.id)


# Test to delete a tour
# run this command:python manage.py test swelocaltoursapi.tests.test_tours

    def test_delete_tour(self):
        """Test delete tour
        """
        tour = Tour.objects.first()
        
        url = f'/tours/{tour.id}'
        response = self.client.delete(url)
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        
        response =self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
