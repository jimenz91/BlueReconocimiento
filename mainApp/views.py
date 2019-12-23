from django.shortcuts import render, redirect, get_object_or_404
from mainApp.models import Mencion, Categoria
from django.db.models import Aggregate, Avg, Count
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from mainApp.choices import categorias, puntuaciones
from django.contrib.auth import get_user_model

User = get_user_model()

def promedio_por_categorias(empleado, pk, menciones):
    """Método para calcular el promedio de las menciones recibidas por un usuario, dividido por categoría
    para mostrarlas en su gráfico de radar.
    """
    agregado = 0
    promedio_total = 0
    # Se obtienen todas las categorías asignadas al usuario y se recorren una por una. Se crea una lista con todas las menciones y se devuelve la lista.
    for categoria in empleado.categorias.all():
        id_categoria = categoria.id
        promedio_cat = Mencion.objects.filter(receptor=pk, categoria=id_categoria).aggregate(Avg('puntuacion__valor'))
        menciones[categoria.nombre] = promedio_cat['puntuacion__valor__avg']
        agregado = agregado + menciones[categoria.nombre]

    return menciones

def crear_menciones(request, pk, empleado):
    """
    Método para crear menciones nuevas para los usuarios, recibiendo las puntuaciones que se quieren aceptar y el empleado receptor.
    """
    user_id = request.user.id
    categorias_empleado = empleado.categorias.all()

    menciones_creadas = []

    for campo in categorias_empleado:
        puntuacion = request.POST[campo.nombre]
        categoria = categorias[campo.nombre]
        puntuacion_id = puntuaciones[puntuacion]
        mencion = Mencion(emisor_id=user_id, categoria_id=categoria, puntuacion_id=puntuacion_id, receptor_id=pk)
        mencion.save()
        menciones_creadas.append(mencion)

    return menciones_creadas

def promedios_totales():
    """
    Método para calcular el promedio de todas las menciones de todos los usuarios y actualizar el campo de promedio.
    Permite la actualización del ranking para mostrarlo en el índice.
    """
    n_empleados = User.objects.count()
    i = 1
    while (i<=n_empleados):
        promedio_total = Mencion.objects.filter(receptor=i).aggregate(Avg('puntuacion__valor'))
        empleado = get_object_or_404(User, pk=i)
        empleado.promedio_puntuaciones = promedio_total['puntuacion__valor__avg']
        empleado.save()
        i += 1

def index(request):
    promedios_totales()

    empleados = User.objects.order_by('-promedio_puntuaciones').filter(activo=True)

    context = {
        'empleados': empleados,
    }

    return render(request, 'index.html', context)

def registro(request):

    if request.method == "POST":
        nombre = request.POST['nombre_registro']
        apellido = request.POST['apellido_registro']
        email = request.POST['email_registro']
        contraseña = request.POST['contraseña_registro']
        contraseña2 = request.POST['contraseña_registro2']
        usuario = request.POST['usuario_registro']

        # Se revisa si las contraseñas son idénticas.
        if contraseña == contraseña2:
            if User.objects.filter(email=email).exists():
                print("Este correo ya está siendo usado.")
            else:
                # Se crea el nuevo usuario en la BBDD.
                user = User.objects.create_user(username=usuario, email=email, first_name=nombre, last_name=apellido)
                user.save()
            return redirect('registro')

        else:
            print("Las contraseñas no coinciden.")
            return redirect('register')

    return render(request, 'registro.html')

def perfil(request, pk):
    promedios_totales()

    empleado = get_object_or_404(User, pk=pk)
    menciones = {}

    if Mencion.objects.filter(receptor=pk):

        menciones = promedio_por_categorias(empleado, pk, menciones)

        if request.method == 'POST':
            if request.user.is_authenticated:
                
                crear_menciones(request, pk, empleado)

                return redirect('perfil', pk)
    
    else:
        if request.method == 'POST':
            if request.user.is_authenticated:
                
                crear_menciones(request, pk, empleado)

                return redirect('perfil', pk)
            

    context = {
        'empleado': empleado,
        'menciones': menciones,
    }

    return render(request, 'perfil.html', context)

def login(request):
    return redirect(request, 'dashboard.html')

def logout(request):
    return redirect('index')

def dashboard(request):
    return render(request, 'dashboard.html')