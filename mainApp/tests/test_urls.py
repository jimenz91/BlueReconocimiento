from django.test import TestCase
from django.urls import resolve, reverse
from mainApp.views import (dashboard, empleados, index, loginv, logoutv,
                           perfil, registro)


class TestUrls(TestCase):

    def test_login_url_resolves(self):
        url = reverse('loginv')
        self.assertEqual(resolve(url).func, loginv)

    def test_logout_url_resolves(self):
        url = reverse('logoutv')
        self.assertEqual(resolve(url).func, logoutv)

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)

    def test_registro_url_resolves(self):
        url = reverse('registro')
        self.assertEqual(resolve(url).func, registro)

    def test_perfil_url_resolves(self):
        url = reverse('perfil', args=[1, ])
        self.assertEqual(resolve(url).func, perfil)

    def test_dashboard_url_resolves(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func, dashboard)

    def test_empleados_url_resolves(self):
        url = reverse('empleados')
        self.assertEqual(resolve(url).func, empleados)
