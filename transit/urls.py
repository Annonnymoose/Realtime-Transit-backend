from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'agencies', views.AgencyViewSet)
router.register(r'calendars', views.CalendarViewSet)
router.register(r'routes', views.RouteViewSet)
router.register(r'stops', views.StopViewSet)
router.register(r'trips', views.TripViewSet)
router.register(r'stop_times', views.StopTimeViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]