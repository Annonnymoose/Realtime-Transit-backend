from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from rest_framework_gis.filters import DistanceToPointFilter
from rest_framework import viewsets
from .models import Agency, Calendar, Route, Stop, Trip, StopTime
from .serializers import (
    AgencySerializer, CalendarSerializer, RouteSerializer, 
    StopSerializer, TripSerializer, StopTimeSerializer, DepartureSerializer
)

# 1. Standard ViewSets
class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

# 2. The Massive Table ViewSet
class StopTimeViewSet(viewsets.ModelViewSet):
    queryset = StopTime.objects.all()
    serializer_class = StopTimeSerializer

# 3. The Spatial ViewSet
class StopViewSet(viewsets.ModelViewSet):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer
    filter_backends = [DistanceToPointFilter]
    distance_filter_field = 'location'
    distance_filter_convert_meters = True

    # This creates a custom endpoint at /api/stops/<id>/departures/
    @action(detail=True, methods=['get'])
    def departures(self, request, pk=None):
        # 1. Grab the specific bus stop the user clicked on
        stop = self.get_object()
        
        # 2. Get the current time on the server (formatted as HH:MM:SS to match GTFS)
        now = datetime.now().strftime("%H:%M:%S")

        # 3. THE ENTERPRISE QUERY
        # - Filter for this exact stop
        # - Filter for times greater than or equal to right now
        # - Use select_related to execute the SQL JOIN (The N+1 killer!)
        # - Order chronologically and slice the top 10 results
        upcoming_stops = StopTime.objects.filter(
            stop=stop,
            arrival_time__gte=now
        ).select_related('trip', 'trip__route').order_by('arrival_time')[:10]

        # 4. Pass the data to our new custom serializer
        serializer = DepartureSerializer(upcoming_stops, many=True)
        return Response(serializer.data)