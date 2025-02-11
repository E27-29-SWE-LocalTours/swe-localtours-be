from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from swelocaltoursapi.models import Location, Tour


# Tour Serializer (used for embedding tours in the location response)
class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ('id', 'name', 'price', 'image', 'description', 'date', 'time', 'duration')


# Location Serializer (used for listing multiple locations)
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'coordinates', 'uid')


# Single Location Serializer (used for retrieving a single location with its associated tours)
class SingleLocationSerializer(serializers.ModelSerializer):
    tour_count = serializers.SerializerMethodField()
    tours = TourSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'coordinates', 'uid', 'tour_count', 'tours')

    def get_tour_count(self, obj):
        """Returns the count of tours related to the location"""
        return Tour.objects.filter(location=obj).count()


# Location ViewSet
class LocationView(viewsets.ViewSet):
    def retrieve(self, request, pk):
        """Handle GET requests for a single location and its associated tours"""
        try:
            location = Location.objects.get(pk=pk)
            serializer = SingleLocationSerializer(location)
            return Response(serializer.data)
        except Location.DoesNotExist:
            return Response({'message': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """Handle GET requests for all locations with optional filtering by 'uid'"""
        uid = request.query_params.get('uid', None)
        locations = Location.objects.all()

        if uid:
            locations = locations.filter(uid=uid)

        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a new location"""
        location = Location.objects.create(
            name=request.data["name"],
            address=request.data["address"],
            coordinates=request.data["coordinates"],
            uid=request.data["uid"]
        )

        serializer = LocationSerializer(location)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests to update an existing location"""
        try:
            location = Location.objects.get(pk=pk)
            location.name = request.data["name"]
            location.address = request.data["address"]
            location.coordinates = request.data["coordinates"]
            location.uid = request.data["uid"]

            location.save()
            serializer = LocationSerializer(location)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Location.DoesNotExist:
            return Response({'message': 'Location not Found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """Handle DELETE requests to delete a location"""
        try:
            location = Location.objects.get(pk=pk)
            location.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Location.DoesNotExist:
            return Response({'message': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)
