from datetime import time, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from bookings.models import Booking, Studio


class DashboardIndexTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice', password='Pa$$w0rd-test'
        )
        self.studio = Studio.objects.create(name='Studio A', hourly_rate=1500)
        self.url = reverse('dashboard:index')

    def _make_booking(self, *, status, days_offset):
        return Booking.objects.create(
            user=self.user,
            studio=self.studio,
            date=timezone.localdate() + timedelta(days=days_offset),
            start_time=time(12, 0),
            duration_hours=2,
            status=status,
        )

    def test_anonymous_redirected_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_active_future_booking_appears_in_active_section(self):
        booking = self._make_booking(status='active', days_offset=5)
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(booking, response.context['active_bookings'])
        self.assertNotIn(booking, response.context['past_bookings'])

    def test_active_past_booking_appears_in_history(self):
        booking = self._make_booking(status='active', days_offset=-5)
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(booking, response.context['past_bookings'])
        self.assertNotIn(booking, response.context['active_bookings'])

    def test_cancelled_booking_appears_in_history(self):
        booking = self._make_booking(status='cancelled', days_offset=2)
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertIn(booking, response.context['past_bookings'])

    def test_completed_booking_appears_in_history(self):
        booking = self._make_booking(status='completed', days_offset=2)
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertIn(booking, response.context['past_bookings'])

    def test_past_count_counts_all_past_not_capped_at_five(self):
        for offset in range(-7, 0):
            self._make_booking(status='completed', days_offset=offset)
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.context['past_count'], 7)
        self.assertEqual(len(response.context['past_bookings']), 5)

    def test_only_current_users_bookings_counted(self):
        other = User.objects.create_user(
            username='bob', password='Pa$$w0rd-test'
        )
        Booking.objects.create(
            user=other, studio=self.studio,
            date=timezone.localdate() + timedelta(days=3),
            start_time=time(10, 0), duration_hours=2, status='active',
        )
        Booking.objects.create(
            user=other, studio=self.studio,
            date=timezone.localdate() - timedelta(days=3),
            start_time=time(10, 0), duration_hours=2, status='completed',
        )
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.context['total_count'], 0)
