from django.db import models 
from django.core.validators import MinValueValidator
from .location import Location
from .user import User
from datetime import timedelta, time


class Tour(models.Model):
 
 user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tours')
 image = models.URLField()
 price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0.00)])
 location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='tours')
 name = models.CharField(max_length=50)
 description = models.CharField(max_length=280)
 date = models.DateField()
 time = models.TimeField(default=time(12, 0))
 duration = models.IntegerField(default=60)  # Store duration in minutes (60 for 1 hour)

 