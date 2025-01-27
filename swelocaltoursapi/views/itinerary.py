from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from swelocaltoursapi.models import Itinerary, Tour, User

class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = ('id', 'user', 'tour', 'completed')

class SingleItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = ('id', 'user', 'tour', 'completed')

class ItineraryView(ViewSet):
    def retrieve(self, request, pk):
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            serializer = SingleItinerarySerializer(itinerary)
            return Response(serializer.data)
        except Itinerary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        itineraries = Itinerary.objects.all()
        serializer = ItinerarySerializer(itineraries, many=True)  
        return Response(serializer.data)  
    
    def create(self, request):
        try:
            user = User.objects.get(pk=request.data["user_id"])
            tour = Tour.objects.get(pk=request.data["tour_id"])
            
            itinerary = Itinerary.objects.create(
                user=user,
                tour=tour,
                completed=request.data.get("completed", False)
            )
            
            serializer = ItinerarySerializer(itinerary)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (User.DoesNotExist, Tour.DoesNotExist):
            return Response({'message': 'Invalid user or tour'}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            
            user = User.objects.get(pk=request.data["user_id"])
            tour = Tour.objects.get(pk=request.data["tour_id"])
            
            itinerary.user = user
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
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            
            itinerary.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Itinerary.DoesNotExist:
            return Response({'message': 'Itinerary not found'}, status=status.HTTP_404_NOT_FOUND)
        