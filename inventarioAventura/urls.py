"""
URL configuration for inventarioAventura project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from cuentas import views as cuentas_views
from experiencias import views as exp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', cuentas_views.SignUpView.as_view(), name='signup'),

    path('', core_views.home, name='home'),

    path('usuarios/', cuentas_views.UsuarioListView.as_view(), name='lista_usuarios'),
    path('usuarios/crear/', cuentas_views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:id>/', cuentas_views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', cuentas_views.eliminar_usuario, name='eliminar_usuario'),

    path('categorias/', exp_views.CategoriaListView.as_view(), name='lista_categorias'),
    path('categorias/crear/', exp_views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:id>/', exp_views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:id>/', exp_views.eliminar_categoria, name='eliminar_categoria'),

    path('experiencias/', exp_views.ExperienciaListView.as_view(), name='lista_experiencias'),
    path('experiencias/crear/', exp_views.crear_experiencia, name='crear_experiencia'),
    path('experiencias/editar/<int:id>/', exp_views.editar_experiencia, name='editar_experiencia'),
    path('experiencias/eliminar/<int:id>/', exp_views.eliminar_experiencia, name='eliminar_experiencia'),

    path('inscripciones/', exp_views.InscripcionListView.as_view(), name='lista_inscripciones'),
    path('inscripciones/inscribir/<int:experiencia_id>/', exp_views.inscribir_experiencia, name='inscribir_experiencia'),
    path('inscripciones/confirmar/<int:id>/', exp_views.cambiar_estado_pago, name='cambiar_estado_pago'),
    path('inscripciones/eliminar/<int:id>/', exp_views.eliminar_inscripcion, name='eliminar_inscripcion'),
]
