from mainApp.models import Categoria, Puntuacion, Proyecto
from django.template.defaultfilters import lower, upper

n_categorias = Categoria.objects.all().values()
n_puntuaciones = Puntuacion.objects.all().values()
n_proyectos = Proyecto.objects.all().values()

categorias = {}
puntuaciones = {}
proyectos = {}

for c in n_categorias:
    categorias[c['nombre']] = c['id']


for p in n_puntuaciones:
    puntuacion = lower(p['denominacion'])
    puntuaciones[puntuacion] = p['id']
    puntuacion = upper(p['denominacion'])
    puntuaciones[puntuacion] = p['id']

puntuaciones[''] = 6

for p in n_proyectos:
    proyectos[p['nombre']] = p['id']
