from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    coordinates = models.JSONField(default=dict)
    uid = models.CharField(max_length=50)
