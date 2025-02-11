from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from swelocaltoursapi.models import Itinerary, Tour, Location, User


# Tour Serializer (for embedding tour details in the Itinerary response)
class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ('id', 'name', 'date', 'time', 'price')


# Location Serializer (for embedding location details in the Tour response)
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'coordinates')


# Itinerary Serializer (used for listing itineraries, including associated tours and locations)
class ItinerarySerializer(serializers.ModelSerializer):
    tour = TourSerializer()  # Include tour details
    completed = serializers.BooleanField()

    class Meta:
        model = Itinerary
        fields = ('id', 'user_id', 'tour', 'completed')


# Single Itinerary Serializer (for retrieving a single itinerary with embedded tour and location)
class SingleItinerarySerializer(serializers.ModelSerializer):
    tour = TourSerializer()  # Include tour details
    location = LocationSerializer(source='tour.location')  # Embed the location of the tour
    completed = serializers.BooleanField()

    class Meta:
        model = Itinerary
        fields = ('id', 'user_id', 'tour', 'location', 'completed')


# Itinerary ViewSet (handles CRUD operations for itineraries)
class ItineraryView(ViewSet):
    def retrieve(self, request, pk):
        """Retrieve a single itinerary with tour and location details"""
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            serializer = SingleItinerarySerializer(itinerary)
            return Response(serializer.data)
        except Itinerary.DoesNotExist:
            return Response({'message': 'Itinerary not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """List all itineraries with optional filtering by location_id and completed status"""
        location_id = request.query_params.get('location_id', None)
        completed = request.query_params.get('completed', None)
        
        itineraries = Itinerary.objects.all()
        
        if location_id:
            itineraries = itineraries.filter(tour__location_id=location_id)
            
        if completed is not None:
            itineraries = itineraries.filter(completed=completed.lower() == 'true')

        serializer = ItinerarySerializer(itineraries, many=True)
        return Response(serializer.data)  
    
    def create(self, request):
        """Create a new itinerary"""
        try:
            user = User.objects.get(pk=request.data["user_id"])
            tour = Tour.objects.get(pk=request.data["tour"])
            
            itinerary = Itinerary.objects.create(
                user_id=user,
                tour=tour,
                completed=request.data.get("completed", False)
            )
            
            serializer = ItinerarySerializer(itinerary)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (User.DoesNotExist, Tour.DoesNotExist):
            return Response({'message': 'Invalid user or tour'}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        """Update an existing itinerary"""
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            
            user = User.objects.get(pk=request.data["user_id"])
            tour = Tour.objects.get(pk=request.data["tour"])
            
            itinerary.user_id = user
            itinerary.tour = tour
            itinerary.completed = request.data.get("completed", itinerary.completed)
            
            itinerary.save()
            serializer = ItinerarySerializer(itinerary)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Itinerary.DoesNotExist:
            return Response({'message': 'Itinerary not found'}, status=status.HTTP_404_NOT_FOUND)
        except (User.DoesNotExist, Tour.DoesNotExist):
            return Response({'message': 'Invalid user or tour'}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        """Delete an itinerary"""
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            itinerary.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Itinerary.DoesNotExist:
            return Response({'message': 'Itinerary not found'}, status=status.HTTP_404_NOT_FOUND)
