from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('ride-history/', views.ride_history, name='ride_history'),
    path('search-routes/', views.search_routes, name='search_routes'),
    path('fare-checker/', views.fare_checker, name='fare_checker'),
    path('metro-schedules/', views.metro_schedules, name='metro_schedules'),
    path('book-ticket/<int:trip_id>/<int:from_station_id>/<int:to_station_id>/', views.book_ticket, name='book_ticket'),
    path('payment-success/<int:ticket_id>/', views.payment_success, name='payment_success'),
    path('offers/', views.offers, name='offers'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='metro/login.html'), name='login'),
    path('profile/', views.profile_view, name='profile'),
    
]