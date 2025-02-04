from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from swelocaltoursapi.models import Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'uid')

class SingleLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'uid')

class LocationView(ViewSet):
    def retrieve(self, request, pk):
        
        try:
            location = Location.objects.get(pk=pk)
            
            serializer = SingleLocationSerializer(location)
            return Response(serializer.data)
        except Location.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        uid = request.query_params.get('uid', None)
        locations = Location.objects.all()
        
        if uid:
            uid = request.query_params.get('uid', None)
            locations = locations.filter(uid=uid)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
        serializer = LocationSerializer(locations, many=True)  
        return Response(serializer.data)  
    
    def create(self, request):
        location = Location.objects.create(
            name=request.data["name"],
            address=request.data["address"],
            uid=request.data["uid"]
        )
        
        serializer = LocationSerializer(location)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        try:
            
            location = Location.objects.get(pk=pk)
            
            location.name = request.data["name"]
            location.address = request.data["address"]
            location.uid = request.data["uid"]
            
            location.save()
            serializer = LocationSerializer(location)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Location.DoesNotExist:
            return Response({'message': 'Location not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        
    def destroy(self, request, pk):
        try:
            location = Location.objects.get(pk=pk)
            
            location.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Location.DoesNotExist:
            return Response({'message': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)    
            
            
        
        
        