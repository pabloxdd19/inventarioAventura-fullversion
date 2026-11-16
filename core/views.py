from django.shortcuts import render
from cuentas.models import Usuario
from experiencias.models import Categoria, Experiencia, Inscripcion


def home(request):
    #  experiencias con categoría activa para mostrar en la bienvenida
    experiencias_activas = Experiencia.objects.filter(categoria__estado='activo')

    context = {
        'experiencias_publicas': experiencias_activas,
        'total_usuarios': Usuario.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'total_experiencias': Experiencia.objects.count(),
        'total_reservas': Inscripcion.objects.count(),
    }
    return render(request, 'home.html', context)