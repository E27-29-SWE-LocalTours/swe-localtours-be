"""View module for handling requests about users"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from swelocaltoursapi.models import User


class UserView(ViewSet):
    """User view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single user"""

        try:
            lt_user = User.objects.get(pk=pk)  
            serializer = UserSerializer(lt_user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all users"""

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations"""

        lt_user = User.objects.create(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            bio=request.data["bio"],
            uid=request.data["uid"]
        )
        serializer = UserSerializer(lt_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for updating a user"""

        try:
            lt_user = User.objects.get(pk=pk)

            # Update fields
            lt_user.first_name = request.data["first_name"]
            lt_user.last_name = request.data["last_name"]
            lt_user.bio = request.data["bio"]
            lt_user.uid = request.data["uid"]
            lt_user.save()

            serializer = UserSerializer(lt_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"message": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except KeyError as e:
            return Response(
                {"message": f"Missing required field: {e.args[0]}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        """Handle DELETE requests to delete a user"""

        try:
            lt_user = User.objects.get(pk=pk)
            lt_user.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'bio', 'uid')
