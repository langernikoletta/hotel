"""
Admin configuration for hotel project.
"""

from django.contrib import admin
from .models import Room, Booking


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'room_type', 'price', 'is_available')
    list_filter = ('room_type', 'is_available')
    search_fields = ('number',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest_name', 'room', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('guest_name', 'guest_email')
    readonly_fields = ('created_at',)
