"""Регистрация моделей в админ-панели Django."""
from django.contrib import admin
from .models import Studio, Booking


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'hourly_rate', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'studio', 'date',
                    'start_time', 'duration_hours', 'status')
    list_filter = ('status', 'date', 'studio')
    search_fields = ('user__username', 'studio__name')
