# Register your models here.
from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Agency, Calendar, Route, Stop, Trip, StopTime

# Register standard models
admin.site.register(Agency)
admin.site.register(Calendar)
admin.site.register(Route)
admin.site.register(Trip)
admin.site.register(StopTime)

# Register the spatial model with the interactive map!
@admin.register(Stop)
class StopAdmin(GISModelAdmin):
    list_display = ('stop_id', 'stop_name')
    search_fields = ('stop_name',)