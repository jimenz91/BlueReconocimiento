from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('perfil/<int:pk>', views.perfil, name='perfil'),
    path('logout/', views.logoutv, name='logoutv'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.loginv, name='loginv'),
]
