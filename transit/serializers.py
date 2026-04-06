from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Agency, Calendar, Route, Stop, Trip, StopTime

# 1. Standard Serializers
# We use standard ModelSerializers for normal, non-spatial data.
# `fields = '__all__'` is a fast way to say "translate every single column in this table."

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

class StopTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopTime
        fields = '__all__'

# 2. Spatial Serializer
# We specifically use GeoFeatureModelSerializer for the Stop model
# so that the spatial PointField is formatted perfectly for web maps!

class StopSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Stop
        geo_field = "location"
        fields = ('stop_id', 'stop_name')


class DepartureSerializer(serializers.ModelSerializer):
    # We are telling DRF: "Go inside the Trip table, then inside the Route table, 
    # and grab the route_long_name so humans can read it!"
    route_name = serializers.CharField(source='trip.route.route_long_name', read_only=True)
    head_sign = serializers.CharField(source='trip.head_sign', read_only=True)

    class Meta:
        model = StopTime
        fields = ('arrival_time', 'route_name', 'head_sign')