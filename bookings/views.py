"""Представления приложения bookings."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm


@login_required
def booking_create(request):
    """Создание новой брони."""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request,
                             f'Бронь №{booking.id} успешно оформлена.')
            return redirect('dashboard:index')
    else:
        form = BookingForm()
    return render(request, 'bookings/booking_form.html', {'form': form})


@login_required
def booking_cancel(request, pk):
    """Отмена брони."""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if not booking.can_be_cancelled():
        messages.error(request, 'Эту бронь уже нельзя отменить.')
        return redirect('dashboard:index')

    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request,
                         f'Бронь №{booking.id} отменена.')
        return redirect('dashboard:index')

    return render(request, 'bookings/booking_cancel.html',
                  {'booking': booking})
