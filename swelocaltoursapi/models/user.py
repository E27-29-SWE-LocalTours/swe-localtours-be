from django.db import models

class User(models.Model):
  
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  bio = models.CharField(max_length=280)
  uid = models.CharField(max_length=50)
  

