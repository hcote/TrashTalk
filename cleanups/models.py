from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from .constants import COUNTRY_CODE_MAP, STATE_CODE_MAP
from .utils import Coordinates


class Cleanup(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    image = models.CharField(max_length=300)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cleanups")
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

    participants = models.ManyToManyField(User)

    def __str__(self):
        return "Cleanup at {0}".format(self.location)

    @property
    def gmap_query(self):
        """For street queries."""
        # TODO: Issue #12 - Add cross street queries when implemented.
        if self.location and self.location.cross_street:
            return "{0}:{1}, {2}".format(self.location.street,
                                         self.location.cross_street, self.city)
        else:
            return self.address

    @property
    def address(self):
        return "{0}+{1},{2}+{3}".format(self.location.street,
                                        self.location.city, self.location.state,
                                        self.location.zipcode)

    def check_name(self):
        if not self.name:
            self.name = self.location

    @property
    def event_start(self):
        """User friendly time. Convert event times to 12-hr format."""
        return datetime.strptime(str(self.start_time), '%X').strftime('%I:%M %p')

    @property
    def event_end(self):
        """User friendly time. Convert event times to 12-hr format."""
        return datetime.strptime(str(self.end_time), '%X').strftime('%I:%M %p')


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

    def __str__(self):
        return "{0} {1}, {2}".format(self.street, self.cross_street, self.city)

    @property
    def address(self):
        return "{} {}".format(self.number, self.street)

    @property
    def coordinates(self):
        return Coordinates(self.latitude, self.longitude)

    @property
    def state_code(self):
        if not self.has_state_code():
            return STATE_CODE_MAP[self.state]
        return self.state

    @property
    def country_code(self):
        if not self.has_country_code():
            self.country = COUNTRY_CODE_MAP[self.country]
        return self.country

    def has_country_code(self):
        return len(self.country) < 3

    def has_state_code(self):
        return len(self.state) < 3
