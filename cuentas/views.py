from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView
from .models import Usuario
from .forms import UsuarioForm, SignUpForm


# Vista para el registro público (usa registration/signup.html)
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


# Listado de usuarios (Solo Administrador)
class UsuarioListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Usuario
    template_name = 'cuentas/usuarios.html'
    context_object_name = 'usuarios'

    def test_func(self):
        return self.request.user.rol == 'admin'


@login_required
def crear_usuario(request):
    if request.user.rol != 'admin':
        return redirect('home')
    form = UsuarioForm()
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('lista_usuarios')
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Registrar Nuevo Usuario'})


@login_required
def editar_usuario(request, id):
    if request.user.rol != 'admin':
        return redirect('home')
    usuario = get_object_or_404(Usuario, id=id)
    form = UsuarioForm(instance=usuario)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('lista_usuarios')
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Editar Usuario'})


@login_required
def eliminar_usuario(request, id):
    if request.user.rol != 'admin':
        return redirect('home')
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    return redirect('lista_usuarios')