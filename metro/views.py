from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import *
from .forms import *
from django.utils import timezone  # For timezone-aware datetime
from .forms import (              # Import all your forms
    ProfileForm,
    TicketForm,
    LoginForm,
    RouteSearchForm,
    FareCheckForm
)
from .models import (             # Import your models if not already present
    User,
    Station,
    Route,
    Train,
    Trip,
    Ticket,
    Payment
)
from .models import User, Station, Route, Trip, Ticket
from .forms import ProfileForm, TicketForm, LoginForm
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm  
from .models import User 
from .forms import UserRegistrationForm
from .models import Schedule
from django.contrib.auth import authenticate, login
from .forms import RouteSearchForm 

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'metro/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'metro/login.html')

def metro_schedules(request):
    schedules = Schedule.objects.all()
    return render(request, 'metro/schedules.html', {'schedules': schedules})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'metro/profile.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'metro/profile.html', {
        'user': request.user
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to your home page
    else:
        form = UserCreationForm()
    return render(request, 'metro/register.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('home')  # Redirect to your homepage after logout


def home(request):
    return render(request, 'metro/home.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 1:  # Admin
                    return redirect('admin_dashboard')
                else:
                    return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user).order_by('-purchase_date')
    return render(request, 'dashboard.html', {'user': user, 'tickets': tickets})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

@login_required
def ride_history(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-purchase_date')
    return render(request, 'ride_history.html', {'tickets': tickets})

def search_routes(request):
    form = RouteSearchForm(request.POST or None)
    trips = []  # Initialize an empty list for trips

    if request.method == 'POST' and form.is_valid():
        from_station = form.cleaned_data['from_station']
        to_station = form.cleaned_data['to_station']
        date = form.cleaned_data['date']
        selected_train = form.cleaned_data.get('train')  # Get the optional train

        if selected_train:
            current_location = selected_train.current_location
            route = selected_train.route

            if current_location == from_station:
                # Find the order of from_station and to_station on the train's route
                try:
                    from_rs = RouteStation.objects.get(route=route, station=from_station)
                    to_rs = RouteStation.objects.get(route=route, station=to_station)
                    if from_rs.order < to_rs.order:
                        route_trips = Trip.objects.filter(
                            route=route.name,  # Assuming Trip.route is CharField
                            departure_time__date=date,
                            status='scheduled'
                        ).filter(departure_time__gte=timezone.now())  # Consider current time
                        # Further filter trips based on the sequence of stations if needed
                        trips = [{'trip': trip, 'fare': Fare.objects.filter(from_station=from_station, to_station=to_station).first().amount if Fare.objects.filter(from_station=from_station, to_station=to_station).first() else 0, 'from_station': from_station, 'to_station': to_station, 'departure_time': trip.departure_time, 'arrival_time': trip.arrival_time} for trip in route_trips]
                except RouteStation.DoesNotExist:
                    pass  # Stations not on the same route or incorrect order

        else:
            # Original logic to search by from and to station (if no train selected)
            valid_routes = []
            routes = Route.objects.filter(routestation__station=from_station).filter(routestation__station=to_station).distinct()
            for route in routes:
                from_rs = route.routestation_set.filter(station=from_station).first()
                to_rs = route.routestation_set.filter(station=to_station).first()
                if from_rs and to_rs and from_rs.order < to_rs.order:
                    valid_routes.append(route)
            for route in valid_routes:
                route_trips = Trip.objects.filter(
                    route=route.name,  # Assuming Trip.route is CharField
                    departure_time__date=date,
                    status='scheduled'
                )
                trips.extend([{'trip': trip, 'fare': Fare.objects.filter(from_station=from_station, to_station=to_station).first().amount if Fare.objects.filter(from_station=from_station, to_station=to_station).first() else 0, 'from_station': from_station, 'to_station': to_station, 'departure_time': trip.departure_time, 'arrival_time': trip.arrival_time} for trip in route_trips])

        return render(request, 'search_results.html', {
            'form': form,  # Pass the form back to the template (even after submission)
            'trips': trips,
            'from_station': from_station,
            'to_station': to_station,
            'date': date,
        })
    else:
        return render(request, 'metro/search_routes.html', {'form': form})

@login_required
def fare_checker(request):
    if request.method == 'POST':
        form = FareCheckForm(request.POST)
        if form.is_valid():
            from_station = form.cleaned_data['from_station']
            to_station = form.cleaned_data['to_station']
            try:
                fare = Fare.objects.get(
                    from_station=from_station,
                    to_station=to_station
                )
                return render(request, 'fare_result.html', {'fare': fare})
            except Fare.DoesNotExist:
                return render(request, 'fare_result.html', {'error': 'No fare information available'})
    else:
        form = FareCheckForm()
    return render(request, 'fare_checker.html', {'form': form})
@login_required
def book_ticket(request, trip_id, from_station_id, to_station_id):
    trip = Trip.objects.get(id=trip_id)
    from_station = Station.objects.get(id=from_station_id)
    to_station = Station.objects.get(id=to_station_id)
    
    try:
        fare = Fare.objects.get(from_station=from_station, to_station=to_station).amount
    except Fare.DoesNotExist:
        fare = 0
    
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.trip = trip
            ticket.fare = fare
            ticket.save()
            
            # Create payment record
            payment = Payment.objects.create(
                ticket=ticket,
                amount=fare,
                payment_method='Credit Card',  # In real app, get from form
                transaction_id=f"TXN-{ticket.id}-{timezone.now().timestamp()}",
                status='completed'
            )
            
            # Update user points (10 points per $1 spent)
            request.user.points += int(fare * 10)
            request.user.save()
            
            return redirect('payment_success', ticket_id=ticket.id)
    else:
        form = TicketForm()
    
    return render(request, 'book_ticket.html', {
        'form': form,
        'trip': trip,
        'from_station': from_station,
        'to_station': to_station,
        'fare': fare,
    })

@login_required
def payment_success(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'payment_success.html', {'ticket': ticket})

def offers(request):
    offers = Offer.objects.filter(
        start_date__lte=timezone.now().date(),
        end_date__gte=timezone.now().date()
    )
    return render(request, 'offers.html', {'offers': offers})

@user_passes_test(lambda u: u.user_type == 1)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_tickets = Ticket.objects.count()
    total_revenue = sum([p.amount for p in Payment.objects.filter(status='completed')])
    
    recent_tickets = Ticket.objects.order_by('-purchase_date')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    return render(request, 'admin/dashboard.html', {
        'total_users': total_users,
        'total_tickets': total_tickets,
        'total_revenue': total_revenue,
        'recent_tickets': recent_tickets,
        'recent_users': recent_users,
    })
