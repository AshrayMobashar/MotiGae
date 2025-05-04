from django.core.management.base import BaseCommand
from django.utils import timezone
from metro.models import *

class Command(BaseCommand):
    help = 'Populates the database with sample metro data'

    def handle(self, *args, **options):
        self.stdout.write("Creating sample data...")
        
        # 1. Create Stations
        central = Station.objects.create(
            name="Central Station", 
            code="CST",
            latitude=18.9398,
            longitude=72.8355,
            zone="1"
        )
        
        downtown = Station.objects.create(
            name="Downtown Terminal", 
            code="DT",
            latitude=18.9250,
            longitude=72.8345,
            zone="1"
        )
        
        # 2. Create Routes
        blue_line = Route.objects.create(
            name="Blue Line",
            color="#007bff"
        )
        
        # 3. Add Stations to Route
        RouteStation.objects.create(
            route=blue_line,
            station=central,
            order=1,
            arrival_time="06:00:00",
            departure_time="06:02:00"
        )
        
        RouteStation.objects.create(
            route=blue_line,
            station=downtown,
            order=2,
            arrival_time="06:10:00",
            departure_time="06:12:00"
        )
        
        # 4. Create Train
        train1 = Train.objects.create(
            name="Blue Express",
            route=blue_line,
            capacity=200,
            current_location=central
        )
        
        # 5. Create Trip
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        Trip.objects.create(
            train=train1,
            departure_time=tomorrow.replace(hour=6, minute=0),
            arrival_time=tomorrow.replace(hour=6, minute=30),
            available_seats=200,
            status="scheduled"
        )
        
        # 6. Create Fare
        Fare.objects.create(
            from_station=central,
            to_station=downtown,
            amount=2.50
        )
        
        # 7. Create Admin User
        User.objects.create_superuser(
            username="admin",
            email="admin@metro.com",
            password="admin123",
            user_type=1
        )
        
        self.stdout.write(self.style.SUCCESS("Successfully created sample data!"))