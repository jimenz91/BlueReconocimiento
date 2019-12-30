from django.contrib import admin
from mainApp.models import Categoria, Mencion, Proyecto, Puntuacion 
from django.contrib.auth import get_user_model

User = get_user_model()

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_active', 'promedio_puntuaciones', 'menciones_hechas', 'get_proyectos', 'get_categorias')
    list_editable = ('is_active',)
    list_display_links = ('id', 'username')

    def get_categorias(self, obj):
        return "\n".join([c.nombre for c in obj.categorias.all()])

    # def get_menciones(self, obj):
    #     return "\n".join([m.categoria for m in obj.menciones.all()])

    def get_proyectos(self, obj):
        return "\n".join([p.nombre for p in obj.proyectos.all()])

class PuntuacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'denominacion', 'valor')
    list_display_links = ('denominacion',)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre',)
    list_display_links = ('nombre',)
    
    # def get_empleados(self, obj):
    #     return "\n".join([e.nombre+' '+e.apellido for e in obj.empleados.all()])

class MencionAdmin(admin.ModelAdmin):
    list_display = ('id', 'emisor', 'receptor', 'categoria', 'puntuacion', 'fecha_realización')
    list_filter = ('receptor',)
    list_display_links = ('id',)
    list_per_page = 20

class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'codigo', 'dificultad', 'autor')
    list_display_links = ('nombre',)


admin.site.register(User, EmpleadoAdmin)
admin.site.register(Puntuacion, PuntuacionAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Mencion, MencionAdmin)
admin.site.register(Proyecto, ProyectoAdmin)