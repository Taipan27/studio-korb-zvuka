from datetime import time, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from bookings.forms import BookingForm
from bookings.models import Booking, Studio


class StudioModelTests(TestCase):
    def test_str_returns_name(self):
        studio = Studio.objects.create(name='Red Room', hourly_rate=1500)
        self.assertEqual(str(studio), 'Red Room')


class BookingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice', password='Pa$$w0rd-test'
        )
        self.studio = Studio.objects.create(name='Studio A', hourly_rate=1500)

    def _make_booking(self, status='active'):
        return Booking.objects.create(
            user=self.user,
            studio=self.studio,
            date=timezone.localdate() + timedelta(days=2),
            start_time=time(12, 0),
            duration_hours=3,
            status=status,
        )

    def test_total_cost_equals_duration_times_hourly_rate(self):
        booking = self._make_booking()
        self.assertEqual(booking.total_cost, Decimal('4500'))

    def test_can_be_cancelled_true_for_active(self):
        booking = self._make_booking(status='active')
        self.assertTrue(booking.can_be_cancelled())

    def test_can_be_cancelled_false_for_cancelled(self):
        booking = self._make_booking(status='cancelled')
        self.assertFalse(booking.can_be_cancelled())

    def test_can_be_cancelled_false_for_completed(self):
        booking = self._make_booking(status='completed')
        self.assertFalse(booking.can_be_cancelled())


class BookingFormTests(TestCase):
    def setUp(self):
        self.studio = Studio.objects.create(name='Studio A', hourly_rate=1500)

    def _form_data(self, date_value):
        return {
            'studio': self.studio.pk,
            'date': date_value.isoformat(),
            'start_time': '12:00',
            'duration_hours': 2,
            'comment': '',
        }

    def test_valid_with_future_date(self):
        future = timezone.localdate() + timedelta(days=3)
        form = BookingForm(data=self._form_data(future))
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_with_today_date(self):
        today = timezone.localdate()
        form = BookingForm(data=self._form_data(today))
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_with_past_date(self):
        past = timezone.localdate() - timedelta(days=1)
        form = BookingForm(data=self._form_data(past))
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_studio_choices_exclude_inactive(self):
        inactive = Studio.objects.create(
            name='Closed', hourly_rate=1500, is_active=False
        )
        form = BookingForm()
        self.assertNotIn(inactive, form.fields['studio'].queryset)
        self.assertIn(self.studio, form.fields['studio'].queryset)


class BookingCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice', password='Pa$$w0rd-test'
        )
        self.studio = Studio.objects.create(name='Studio A', hourly_rate=1500)
        self.url = reverse('bookings:create')

    def test_anonymous_redirected_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_get_renders_form(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_post_valid_creates_booking_and_redirects_to_dashboard(self):
        self.client.force_login(self.user)
        future = timezone.localdate() + timedelta(days=4)
        before = Booking.objects.count()
        response = self.client.post(self.url, data={
            'studio': self.studio.pk,
            'date': future.isoformat(),
            'start_time': '14:00',
            'duration_hours': 2,
            'comment': '',
        })
        self.assertRedirects(response, reverse('dashboard:index'))
        self.assertEqual(Booking.objects.count(), before + 1)
        booking = Booking.objects.latest('id')
        self.assertEqual(booking.user, self.user)


class BookingCancelViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice', password='Pa$$w0rd-test'
        )
        self.studio = Studio.objects.create(name='Studio A', hourly_rate=1500)
        self.booking = Booking.objects.create(
            user=self.user,
            studio=self.studio,
            date=timezone.localdate() + timedelta(days=3),
            start_time=time(10, 0),
            duration_hours=2,
            status='active',
        )

    def test_anonymous_redirected_to_login(self):
        url = reverse('bookings:cancel', args=[self.booking.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_404_for_other_users_booking(self):
        other = User.objects.create_user(
            username='bob', password='Pa$$w0rd-test'
        )
        other_booking = Booking.objects.create(
            user=other,
            studio=self.studio,
            date=timezone.localdate() + timedelta(days=4),
            start_time=time(11, 0),
            duration_hours=2,
            status='active',
        )
        self.client.force_login(self.user)
        url = reverse('bookings:cancel', args=[other_booking.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_cancels_active_booking(self):
        self.client.force_login(self.user)
        url = reverse('bookings:cancel', args=[self.booking.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('dashboard:index'))
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'cancelled')

    def test_get_on_already_cancelled_redirects_to_dashboard(self):
        self.booking.status = 'cancelled'
        self.booking.save()
        self.client.force_login(self.user)
        url = reverse('bookings:cancel', args=[self.booking.pk])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('dashboard:index'))
