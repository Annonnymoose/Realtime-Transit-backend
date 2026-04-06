# your_app/management/commands/load_gtfs.py
from django.core.management.base import BaseCommand
import csv
from datetime import datetime
from transit.models import *
from django.contrib.gis.geos import Point

class Command(BaseCommand):
    help = 'Loads transit data into the database'

    # The handle method is what runs when you execute the command
    def handle(self, *args, **kwargs):
        self.stdout.write("Starting GTFS Data Ingestion")
    
        # 1. Load Agency
        self.stdout.write("Loading Agencies....")
        with open(r'Data\mdb-1262-202506170152\agency.csv', 'r', encoding='utf-8') as file:
            rd = csv.DictReader(file)
            stc = []
            for row in rd:
                new_agency = Agency(
                    agency_id = row['agency_id'],
                    agency_name = row['agency_name'],
                    agency_timezone = row['agency_timezone']
                )
                stc.append(new_agency)
            Agency.objects.bulk_create(stc, batch_size=5000, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Successfully loaded {len(stc)} agencies"))

        # 2. Load Calendar
        with open(r'Data\mdb-1262-202506170152\calendar.csv', 'r', encoding='utf-8') as file:
            rd = csv.DictReader(file)
            stc = []
            for row in rd:
                new_calendar = Calendar(
                    service_id = row['service_id'],
                    monday = bool(int(row['monday'])),
                    tuesday = bool(int(row['tuesday'])),
                    wednesday = bool(int(row['wednesday'])),
                    thursday = bool(int(row['thursday'])),
                    friday = bool(int(row['friday'])),
                    saturday = bool(int(row['saturday'])),
                    sunday = bool(int(row['sunday'])),
                    
                    start_date = datetime.strptime(row['start_date'], '%Y%m%d').date(),
                    end_date = datetime.strptime(row['end_date'], '%Y%m%d').date()
                )
                stc.append(new_calendar)
            Calendar.objects.bulk_create(stc, batch_size=5000, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Successfully loaded {len(stc)} calendar"))

        # 3. Load Route
        with open(r'Data\mdb-1262-202506170152\routes.csv', 'r', encoding='utf-8') as file:
            rd = csv.DictReader(file)
            stc = []
            for row in rd:
                new_route = Route(
                    agency_id = row['agency_id'],
                    route_id = row['route_id'],
                    route_short_name = row['route_short_name'],
                    route_long_name = row['route_long_name']
                )
                stc.append(new_route)
            Route.objects.bulk_create(stc, batch_size=5000, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Successfully loaded {len(stc)} route"))

        # 4. Load Stop
        with open(r'Data\mdb-1262-202506170152\stops.csv', 'r', encoding='utf-8') as file:
            rd = csv.DictReader(file)
            stc = []
            for row in rd:
                # 1. Extract the raw lat/lon from the CSV and Transform it into a spatial Point
                spatial_point = Point(float(row['stop_lon']), float(row['stop_lat']), srid=4326)

                new_stop = Stop(
                    stop_id = row['stop_id'],
                    stop_name = row['stop_name'],
                    location = spatial_point
                )
                stc.append(new_stop)
            Stop.objects.bulk_create(stc, batch_size=5000, ignore_conflicts=True)   
            self.stdout.write(self.style.SUCCESS(f"Successfully loaded {len(stc)} stops"))         
        
        # 5. Load Trip
        with open(r'Data\mdb-1262-202506170152\trips.csv', 'r', encoding='utf-8') as file:
            rd = csv.DictReader(file)
            stc = []
            for row in rd:
                new_trip = Trip(
                    route_id = row['route_id'], # the '_id' appended to it for every Foriegn key
                    trip_id = row['trip_id'],
                    head_sign = row.get('trip_headsign', ''),
                    direction = int(row.get('direction_id', 0)) if row.get('direction_id') else 0
                )
                stc.append(new_trip)
            Trip.objects.bulk_create(stc, batch_size=5000, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Successfully loaded {len(stc)} trips"))

        # 6. Load Stop Time
        self.stdout.write("Loading Stop Times (Chunked)...")
        with open(r'Data\mdb-1262-202506170152\stop_times.csv', 'r', encoding='utf-8') as file:
            rd = csv.DictReader(file)
            stc = []
            
            for index, row in enumerate(rd):
                new_stop_time = StopTime(
                    trip_id = row['trip_id'],
                    stop_id = row['stop_id'],
                    arrival_time = row['arrival_time'],
                    departure_time = row['departure_time'],
                    stop_sequence = int(row['stop_sequence'])
                )
                stc.append(new_stop_time)
                
                # Every time we hit 5,000 rows, save them and clear the list!
                if len(stc) == 5000:
                    StopTime.objects.bulk_create(stc, ignore_conflicts=True)
                    self.stdout.write(f"Processed {index + 1} stop times...")
                    stc = [] # <--- This empties the RAM!
            
            # Catch any leftover rows at the very end (e.g., the last 1,432 rows)
            if stc:
                StopTime.objects.bulk_create(stc, ignore_conflicts=True)
                
            self.stdout.write(self.style.SUCCESS("Successfully finished loading all stop times!"))

        self.stdout.write(self.style.SUCCESS(f"Sprint 1 data ingestion complete"))
