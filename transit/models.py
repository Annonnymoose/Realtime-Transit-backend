from django.db import models
from django.contrib.gis.db import models

# Create your models here.
class Agency(models.Model):
    # CharField translated into "VARCHAR" in SQL, max_length is required for CharField
    agency_id = models.CharField(max_length=50, primary_key=True)
    agency_name = models.CharField(max_length=255)
    agency_timezone = models.CharField(max_length=50)
    
    def ___str__(self):
        return self.agency_name

class Calendar(models.Model):
    service_id = models.CharField(max_length=50, primary_key=True)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.service_id

class Route(models.Model):
    route_id = models.CharField(max_length=50, primary_key=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE) # Foriegn Key
    route_short_name = models.CharField(max_length=50)
    route_long_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.route_short_name} - {self.route_long_name}"
    
class Stop(models.Model):
    stop_id = models.CharField(max_length=50, primary_key=True)
    stop_code = models.CharField(max_length=50, null=True, blank=True)
    stop_name = models.CharField(max_length=255)
    stop_lat = models.CharField(max_length=50, null=True, blank=True)
    stop_lon = models.CharField(max_length=50, null=True, blank=True)
    location = models.PointField(srid=4326, null=True, blank=True)

    def __str__(self):
        return self.stop_name

class Trip(models.Model):
    trip_id = models.CharField(max_length=20, primary_key=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)  # Foriegn Key
    head_sign = models.CharField(max_length=255)
    direction = models.IntegerField()
    
    def __str__(self):
        return self.head_sign
    
class StopTime(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)# Foriegn Key
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)# Foriegn Key
    arrival_time = models.CharField(max_length=8)
    departure_time = models.CharField(max_length=8)
    stop_sequence = models.IntegerField()

    def __str__(self):
        # Clean, readable, and handles the integer automatically!
        return f"Arrival: {self.arrival_time} | Departure: {self.departure_time} | Stop Seq: {self.stop_sequence}"