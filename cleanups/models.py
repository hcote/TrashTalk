from django.db import models
from django.contrib.auth.models import User


class Cleanup(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    image = models.CharField(max_length=300)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cleanups")
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

    participants = models.ManyToManyField(User)


class Location(models.Model):
    DEFAULT_CITY = "Oakland"
    DEFAULT_STATE = "California"

    number = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    cross_street = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default=DEFAULT_CITY)
    state = models.CharField(max_length=100, default=DEFAULT_STATE)
    zipcode = models.CharField(max_length=10)
    county = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
