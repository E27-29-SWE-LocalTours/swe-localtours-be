from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from swelocaltoursapi.models import Tour, Location, User


# ViewSet
class TourView(ViewSet):
    def retrieve(self, request, pk):
        """Handle GET requests for a single tour"""
        try:
            tour = Tour.objects.get(pk=pk)
            serializer = SingleTourSerializer(tour)
            return Response(serializer.data)
        except Tour.DoesNotExist:
            return Response({'message': 'Tour not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests for all tours"""
        location_id = request.query_params.get('location', None)
        uid = request.query_params.get('uid', None) 
        tours = Tour.objects.all()
        
        if location_id:
            tours = tours.filter(location_id=location_id)
            
        if uid:
         tours = tours.filter(uid=uid)     
        serializer = TourSerializer(tours, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a new tour"""
        try:
            # Fetch related models
            user = User.objects.get(pk=request.data["user_id"])
            # uid_user = User.objects.get(uid=request.data["uid"])
            location = Location.objects.get(pk=request.data["location"])

            # Create the Tour instance
            tour = Tour.objects.create(
                user_id=user,
                uid=request.data["uid"],
                image=request.data["image"],
                price=request.data["price"],
                location=location,
                name=request.data["name"],
                description=request.data["description"],
                date=request.data["date"],
                time=request.data["time"],
                duration=request.data["duration"]
                
            
            )
            serializer = TourSerializer(tour)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Location.DoesNotExist:
            return Response({"error": "Location not found"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests to update an existing tour"""
        try:
            tour = Tour.objects.get(pk=pk)
            uid_user = User.objects.get(uid=request.data["uid"])
            location = Location.objects.get(pk=request.data["location"])

            # Update fields
            tour.uid = uid_user,
            tour.image = request.data["image"]
            tour.price = request.data["price"]
            tour.location = location
            tour.name = request.data["name"]
            tour.description = request.data["description"]
            tour.date = request.data["date"]
            tour.time = request.data["time"]
            tour.duration = request.data["duration"]
            

            tour.save()
            serializer = TourSerializer(tour)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tour.DoesNotExist:
            return Response({'message': 'Tour not found'}, status=status.HTTP_404_NOT_FOUND)
        except Location.DoesNotExist:
            return Response({'message': 'Location not found'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """Handle DELETE requests to delete a tour"""
        try:
            tour = Tour.objects.get(pk=pk)
            tour.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Tour.DoesNotExist:
            return Response({'message': 'Tour not found'}, status=status.HTTP_404_NOT_FOUND)
# Serializers
class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ('id', 'user_id', 'image', 'price', 'location', 'name', 'description', 'date', 'time', 'duration', 'uid')

class SingleTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ('id', 'user_id', 'image', 'price', 'location', 'name', 'description', 'date', 'time', 'duration', 'uid')
