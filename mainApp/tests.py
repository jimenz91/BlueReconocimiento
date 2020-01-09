from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from .views import (dashboard, empleados, index, loginv, logoutv, perfil,
                    registro)


def sample_user(email='carlosjimenez@bluetab.net', username='carlos',
                password='123pass', first_name='Carlos', last_name='Jiménez'):
    """
    Método para crear un usuario para las pruebas.
    """
    return get_user_model().objects.create_user(email, username,
                                                password, first_name,
                                                last_name)


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


class TestModels(TestCase):

    def test_create_user_with_email_successful(self):
        """Prueba de crear un nuevo usuario con el correo es exitoso."""
        email = 'jimenz91@gmail.com'
        username = 'jimenz'
        password = '123pass'
        nombre = 'carlos'
        apellido = 'Jiménez'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            username=username,
            first_name=nombre,
            last_name=apellido,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.first_name, nombre)
        self.assertEqual(user.last_name, apellido)
        self.assertEqual(user.username, username)

    def test_new_user_email_normalized(self):
        """Se asegura que el correo de un nuevo usuario está normalizado."""
        email = 'test@GMAil.com'
        user = get_user_model().objects.create_user(
                                                    email=email,
                                                    password='test123',
                                                    username='usuario'
                                                    )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Probar que crear un usuario sin un correo genera un error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123', 'usuario')

    def test_create_new_superuser(self):

        email = 'jimenz91@gmail.com'
        username = 'jimenz'
        password = '123pass'
        nombre = 'Carlos'
        apellido = 'Jiménez'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
            username=username,
            first_name=nombre,
            last_name=apellido,
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
