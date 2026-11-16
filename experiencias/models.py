from django.db import models
from cuentas.models import Usuario


class Categoria(models.Model):
    ESTADOS = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=15, choices=ESTADOS, default='activo')

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"


class Experiencia(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.IntegerField()
    cupo_maximo = models.IntegerField()
    fecha_hora = models.DateTimeField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} - ${self.precio}"


class Inscripcion(models.Model):
    ESTADOS_PAGO = (
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    experiencia = models.ForeignKey(Experiencia, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='pendiente')

    def __str__(self):
        return f"{self.usuario.username} -> {self.experiencia.titulo} ({self.get_estado_pago_display()})"
