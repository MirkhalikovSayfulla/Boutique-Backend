from django.test import SimpleTestCase
from django.urls import resolve, reverse

from users.views import login_view, logout_view, register_view


class TestUrls(SimpleTestCase):
    def test_register_url_resolved(self):
        url = reverse('users:register')
        self.assertEqual(resolve(url).func, register_view)

    def test_login_url_resolved(self):
        url = reverse('users:login')
        self.assertEqual(resolve(url).func, login_view)

    def test_logout_url_resolved(self):
        url = reverse('users:logout')
        self.assertEqual(resolve(url).func, logout_view)
