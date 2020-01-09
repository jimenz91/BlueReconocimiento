from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from mainApp.models import Categoria, Mencion, Proyecto, Puntuacion

from .views import (dashboard, empleados, index, loginv, logoutv, perfil,
                    registro)


def sample_user(email='carlosjimenez@bluetab.net', username='carlos',
                password='123pass'):
    """
    Método para crear un usuario para las pruebas.
    """
    return get_user_model().objects.create_user(email, username, password)


def sample_user_2(
        email='andresgomez@bluetab.net',
        username='andres',
        password='123pass'
        ):
    """
    Método para crear un usuario para las pruebas.
    """
    return get_user_model().objects.create_user(email, username, password)


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


class TestUserModel(TestCase):

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
        """Se prueba la creación de un nuevo superusuario."""
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

    def test_user_str(self):
        """Se prueba la representación de los usuarios."""

        usuario = get_user_model().objects.create(
            email='carlosjimenez@bluetab.net',
            password='123pass',
            username='carlos',
            first_name='Carlos',
            last_name='Jiménez'
        )

        self.assertEqual(
            str(usuario),
            usuario.first_name+" "+usuario.last_name
            )


class TestCategoriaModel(TestCase):

    def test_create_categoria(self):
        """Se prueba la creación de una nueva categoría"""

        nombre = 'Soft Skills',
        descripcion = 'Es una categoría'

        categoria = Categoria.objects.create(
            nombre=nombre,
            descripcion=descripcion
        )

        self.assertEqual(categoria.nombre, nombre)
        self.assertEqual(categoria.descripcion, descripcion)

    def test_categoria_str(self):
        """Se prueba la representación de las categorías."""
        categoria = Categoria.objects.create(
            nombre='Soft Skills'
        )

        self.assertEqual(str(categoria), categoria.nombre)


class TestPuntuacionModel(TestCase):

    def test_create_puntuacion(self):
        """Prueba la creación de una nueva puntuación."""
        denomincacion = 'F'
        valor = 0
        descripcion = 'La peor puntuación posible.'

        puntuacion = Puntuacion.objects.create(
            denominacion=denomincacion,
            valor=valor,
            descripcion=descripcion
        )

        self.assertEqual(puntuacion.denominacion, denomincacion)
        self.assertEqual(puntuacion.valor, valor)
        self.assertEqual(puntuacion.descripcion, descripcion)

    def test_puntuacion_verbose_name(self):
        """Se prueba el nombre en plural del modelo."""
        self.assertEqual(
            str(Puntuacion._meta.verbose_name_plural),
            'Puntuaciones')

    def test_puntuacion_str(self):
        """Se prueba la representación de las puntuaciones."""
        puntuacion = Puntuacion.objects.create(
            denominacion='G',
            valor=0
        )

        self.assertEqual(str(puntuacion), puntuacion.denominacion)


class TestProyectoModel(TestCase):

    def test_create_proyecto(self):
        """Se prueba la creación de un nuevo proyecto"""
        nombre = 'Web'
        descripcion = 'Páginas web.'
        codigo = 'BT25'
        dificultad = 10
        autor = sample_user()

        proyecto = Proyecto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            codigo=codigo,
            dificultad=dificultad,
            autor=autor
        )

        self.assertEqual(proyecto.nombre, nombre)
        self.assertEqual(proyecto.descripcion, descripcion)
        self.assertEqual(proyecto.codigo, codigo)
        self.assertEqual(proyecto.dificultad, dificultad)

    def test_proyecto_str(self):
        """Se prueba la representación del nombre del proyecto."""

        proyecto = Proyecto.objects.create(
            nombre='Machine Learning',
            dificultad=10
        )

        self.assertEqual(str(proyecto), proyecto.nombre)


class TestMencionModel(TestCase):

    def test_create_mencion(self):
        """Se prueba la creación de nuevas menciones."""
        emisor = sample_user()
        receptor = sample_user_2()
        categoria = Categoria.objects.create(nombre='Soft Skills')
        puntuacion = Puntuacion.objects.create(
            denominacion='F',
            valor=0,
            descripcion='La peor puntuacion.'
            )

        mencion = Mencion.objects.create(
            emisor=emisor,
            receptor=receptor,
            categoria=categoria,
            puntuacion=puntuacion
        )

        self.assertEqual(mencion.emisor, emisor)
        self.assertEqual(mencion.receptor, receptor)
        self.assertEqual(mencion.categoria, categoria)
        self.assertEqual(mencion.puntuacion, puntuacion)

    def test_menciones_verbose_name(self):
        """Se prueba el nombre emn plural del modelo."""
        self.assertEqual(str(Mencion._meta.verbose_name_plural), 'Menciones')
