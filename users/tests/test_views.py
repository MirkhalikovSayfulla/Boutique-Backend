from django.test import TestCase, Client
from django.urls import reverse


class TestView(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.logout_url = reverse('users:logout')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/login.html')

    def test_logout_view_get(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 200)
