"""URL-маршруты приложения bookings."""
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('new/', views.booking_create, name='create'),
    path('<int:pk>/cancel/', views.booking_cancel, name='cancel'),
]
