from django.contrib.auth import SESSION_KEY
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegisterViewTests(TestCase):
    def setUp(self):
        self.url = reverse('accounts:register')

    def test_get_renders_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_post_valid_creates_user_and_logs_in(self):
        response = self.client.post(self.url, data={
            'username': 'newuser',
            'first_name': 'Иван',
            'email': 'ivan@example.com',
            'password1': 'Pa$$w0rd-test',
            'password2': 'Pa$$w0rd-test',
        })
        self.assertRedirects(response, reverse('dashboard:index'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertIn(SESSION_KEY, self.client.session)

    def test_authenticated_user_redirected_away(self):
        user = User.objects.create_user(
            username='alice', password='Pa$$w0rd-test'
        )
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('dashboard:index'))
