from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from .models import Categoria, Experiencia, Inscripcion
from .forms import CategoriaForm, ExperienciaForm, InscripcionForm



#CATEGORÍAS (Solo Administrador)

class CategoriaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Categoria
    template_name = 'experiencias/categorias.html'
    context_object_name = 'categorias'

    def test_func(self):
        return self.request.user.rol == 'admin'


@login_required
def crear_categoria(request):
    if request.user.rol != 'admin':
        return redirect('home')
    form = CategoriaForm()
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Nueva Categoría'})


@login_required
def editar_categoria(request, id):
    if request.user.rol != 'admin':
        return redirect('home')
    categoria = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(instance=categoria)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Editar Categoría'})


@login_required
def eliminar_categoria(request, id):
    if request.user.rol != 'admin':
        return redirect('home')
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    return redirect('lista_categorias')


#EXPERIENCIAS 
class ExperienciaListView(LoginRequiredMixin, ListView):
    model = Experiencia
    template_name = 'experiencias/experiencias.html'
    context_object_name = 'experiencias'

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'admin':
            return Experiencia.objects.all()
        elif user.rol == 'guia':
            return Experiencia.objects.filter(creador=self.request.user)
        elif user.rol == 'turista':
            return Experiencia.objects.filter(categoria__estado='activo')


@login_required
def crear_experiencia(request):
    if request.user.rol not in ['admin', 'guia']:
        return redirect('home')
    form = ExperienciaForm()
    if request.method == 'POST':
        form = ExperienciaForm(request.POST)
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.creador = request.user
            experiencia.save()
            return redirect('lista_experiencias')
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Registrar Experiencia'})


@login_required
def editar_experiencia(request, id):
    experiencia = get_object_or_404(Experiencia, id=id)
    if request.user.rol == 'guia' and experiencia.creador != request.user:
        return redirect('lista_experiencias')
    if request.user.rol == 'turista':
        return redirect('home')

    form = ExperienciaForm(instance=experiencia)
    if request.method == 'POST':
        form = ExperienciaForm(request.POST, instance=experiencia)
        if form.is_valid():
            form.save()
            return redirect('lista_experiencias')
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Editar Experiencia'})


@login_required
def eliminar_experiencia(request, id):
    if request.user.rol != 'admin':
        return redirect('lista_experiencias')
    experiencia = get_object_or_404(Experiencia, id=id)
    experiencia.delete()
    return redirect('lista_experiencias')


# INSCRIPCIONES 
class InscripcionListView(LoginRequiredMixin, ListView):
    model = Inscripcion
    template_name = 'experiencias/inscripciones.html'
    context_object_name = 'inscripciones'

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'admin':
            return Inscripcion.objects.all()
        elif user.rol == 'guia':
            return Inscripcion.objects.filter(experiencia__creador=user)
        elif user.rol == 'turista':
            return Inscripcion.objects.filter(usuario=user)


@login_required
def inscribir_experiencia(request, experiencia_id):
    experiencia = get_object_or_404(Experiencia, id=experiencia_id)
    Inscripcion.objects.create(
        usuario=request.user,
        experiencia=experiencia,
        estado_pago='pendiente'
    )
    return redirect('lista_inscripciones')


@login_required
def cambiar_estado_pago(request, id):
    inscripcion = get_object_or_404(Inscripcion, id=id)
    if request.user.rol in ['admin', 'turista']:
        inscripcion.estado_pago = 'confirmado'
        inscripcion.save()
    return redirect('lista_inscripciones')


@login_required
def eliminar_inscripcion(request, id):
    inscripcion = get_object_or_404(Inscripcion, id=id)
    if request.user.rol == 'admin' or inscripcion.usuario == request.user:
        inscripcion.delete()
    return redirect('lista_inscripciones')