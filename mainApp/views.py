from django.shortcuts import render, redirect, get_object_or_404
from mainApp.models import Mencion, Categoria
from django.db.models import Aggregate, Avg, Count
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from mainApp.choices import categorias, puntuaciones
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import FormularioRegistro

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

    empleados = User.objects.order_by('-promedio_puntuaciones').filter(is_active=True).exclude(first_name='Admin')

    context = {
        'empleados': empleados,
    }

    return render(request, 'index.html', context)

def registro(request):
    """
    View para registro de usuarios. Cuando un usuario se registra, se realiza el login automáticamente.
    """
    if request.method == "POST":
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            login(request)
                        
            return redirect('dashboard')

        return render(request, 'dashboard')

    else:
        form = FormularioRegistro()
        args = {'form': form}
        return render(request, 'registro.html', args)

def perfil(request, pk):
    """
    View para ver el perfil de otros usuarios, así como la asignación de menciones.
    """
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

def loginv(request):
    """
    View con la lógica de login de usuarios.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                print("Login realizado correctamente.")
                return redirect('dashboard')
            else:
                print("Usuario o contraseña incorrectos.")
                return render(request, 'login.html')

    form = AuthenticationForm()
    args = {'form': form}
    return render(request, 'login.html', args)
    

def logoutv(request):
    """
    View con la lógica de logout de usuarios.
    """
    logout(request)
    print("Lougout successful.")
    return redirect('index')

def dashboard(request):
    """
    View para mostrar la información del usuario logado.
    """

    promedios_totales()

    usuario = request.user
    print(usuario)
    menciones={}

    menciones = promedio_por_categorias(usuario, usuario.id, menciones)

    print(menciones)

    context = {
        'menciones': menciones
    }

    return render(request, 'dashboard.html', context)