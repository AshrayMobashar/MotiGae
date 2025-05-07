from django.contrib import admin
from .models import Schedule, Train, Station, Route
from .models import Fare
from django.contrib.admin.models import LogEntry
from django.utils.translation import gettext_lazy as _
from .models import Station, Route, Train, Schedule, Trip, Fare, Ticket, Payment, Offer, Profile

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'zone')
    search_fields = ('name', 'code')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)
    filter_horizontal = ('stations',) # For ManyToMany field

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('name', 'route', 'capacity', 'current_location')
    list_filter = ('route', 'current_location')
    search_fields = ('name',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('train', 'departure_time', 'arrival_time', 'frequency', 'status')
    list_filter = ('train', 'status')
    search_fields = ('train__name',)

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('route', 'departure_time', 'arrival_time', 'status')
    list_filter = ('status',)
    search_fields = ('route',)

@admin.register(Fare)
class FareAdmin(admin.ModelAdmin):
    list_display = ('from_station', 'to_station', 'amount_bdt')
    search_fields = ('from_station__name', 'to_station__name')
    ordering = ('from_station__name', 'to_station__name')

    def amount_bdt(self, obj):
        return f'৳{obj.amount}'
    amount_bdt.short_description = 'Fare (BDT)'

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'trip', 'purchase_date', 'seat_number', 'fare', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'trip__route')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'amount', 'payment_date', 'payment_method', 'status')
    list_filter = ('status', 'payment_method')
    search_fields = ('ticket__id', 'transaction_id')

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'discount_percentage')
    list_filter = ('start_date', 'end_date')
    search_fields = ('name', 'description')
    filter_horizontal = ('applicable_routes',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'points')
    search_fields = ('user__username', 'phone')