from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelo Empleado
class Empleado(AbstractUser):
    #Opciones de roles
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
        ('ventas', 'Ventas'),
        ('marketing', 'Marketing'),
        ('redes_sociales', 'Redes Sociales'),
        ('desarrollo', 'Desarrollo')
    ]

    rol = models.CharField(max_length=120, choices=ROL_CHOICES, default='admin')
    fecha_nacimiento = models.DateField()
    telefono = models.IntegerField(max_length=9)
    direccion = models.CharField(max_length=120)
    num_seguridad_social = models.IntegerField(max_length=12)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

