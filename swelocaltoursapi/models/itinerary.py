from django.db import models
from .tour import Tour


class Itinerary(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='itineraries')
    date_id = models.DateTimeField()
    completed = models.BooleanField(default=False)
