from django.db import models


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=4000)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name
class Location(models.Model):
    city_name =models.CharField(max_length=50)
    country_name =models.CharField(max_length=50)
    
    def __str__(self):
        return self.city_name