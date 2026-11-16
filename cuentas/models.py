from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('guia', 'Guía / Operador'),
        ('turista', 'Turista / Cliente'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='admin')
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"