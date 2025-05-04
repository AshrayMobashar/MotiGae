from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Admin'),
        (2, 'Staff'),
        (3, 'Passenger'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    points = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    
    def __str__(self):
        return self.username

class Station(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    zone = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Route(models.Model):
    name = models.CharField(max_length=100)
    stations = models.ManyToManyField(Station, through='RouteStation')
    color = models.CharField(max_length=20, default='blue')
    
    def __str__(self):
        return self.name

class RouteStation(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    
    class Meta:
        ordering = ['order']
        unique_together = ('route', 'station', 'order')
    
    def __str__(self):
        return f"{self.route.name} - {self.station.name} (Order: {self.order})"

class Train(models.Model):
    name = models.CharField(max_length=100)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField()
    current_location = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.route.name})"

class Trip(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    available_seats = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=(
        ('scheduled', 'Scheduled'),
        ('departed', 'Departed'),
        ('arrived', 'Arrived'),
        ('cancelled', 'Cancelled'),
    ), default='scheduled')
    
    def __str__(self):
        return f"{self.train.name} - {self.departure_time}"

class Fare(models.Model):
    from_station = models.ForeignKey(Station, related_name='from_fares', on_delete=models.CASCADE)
    to_station = models.ForeignKey(Station, related_name='to_fares', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ('from_station', 'to_station')
    
    def __str__(self):
        return f"{self.from_station.code} to {self.to_station.code}: ${self.amount}"

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    seat_number = models.CharField(max_length=10)
    fare = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, choices=(
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('used', 'Used'),
    ), default='booked')
    
    def __str__(self):
        return f"Ticket #{self.id} - {self.user.username}"

class Payment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ), default='pending')
    
    def __str__(self):
        return f"Payment for Ticket #{self.ticket.id}"

class Offer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    discount_percentage = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    start_date = models.DateField()
    end_date = models.DateField()
    applicable_routes = models.ManyToManyField(Route, blank=True)
    min_points_required = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name