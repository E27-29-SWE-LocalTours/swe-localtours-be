from django.db import models
from .tour import Tour
from .user import User


class Itinerary(models.Model):
    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itineraries' )
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='itineraries')
    completed = models.BooleanField(default=False)
    uid = models.CharField(max_length=50) 
