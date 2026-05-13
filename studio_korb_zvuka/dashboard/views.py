"""Представления приложения dashboard (личный кабинет)."""
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from bookings.models import Booking


@login_required
def index(request):
    """Главная страница личного кабинета пользователя."""
    today = timezone.localdate()
    user_bookings = Booking.objects.filter(user=request.user)
    active_bookings = user_bookings.filter(status='active', date__gte=today)
    past_bookings_qs = user_bookings.filter(
        Q(status__in=['cancelled', 'completed']) | Q(status='active', date__lt=today)
    )
    past_bookings = past_bookings_qs.order_by('-date')[:5]

    context = {
        'active_bookings': active_bookings,
        'past_bookings': past_bookings,
        'total_count': user_bookings.count(),
        'active_count': active_bookings.count(),
        'past_count': past_bookings_qs.count(),
    }
    return render(request, 'dashboard/index.html', context)
