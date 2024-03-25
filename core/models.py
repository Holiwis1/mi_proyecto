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

    rol = models.CharField(max_length=120, choices=ROL_CHOICES, default='admin', null=True)
    fecha_nacimiento = models.DateField(null=True)
    telefono = models.IntegerField(null=True)
    direccion = models.CharField(max_length=120, null=True)
    num_seguridad_social = models.IntegerField(null=True)
    #me falta foto de la persona y foto dni

    def __str__(self):
        return self.first_name + ' ' + self.last_name

#Modelo Cliente
class Cliente(models.Model):
    #Opciones de tipo de cliente
    TIPO_CHOICES = [
        ('empresa', 'Empresa'),
        ('particular', 'Particular'),
        ('proveedor', 'Proveedor'),
        ('leads', 'Leads')
    ]

    nombre = models.CharField(max_length=120)
    nombre_comercial = models.CharField(max_length=120)
    nif = models.CharField(max_length=9)
    tipo = models.CharField(max_length=120, choices=TIPO_CHOICES, default='empresa', null=True)
    razon_social = models.CharField(max_length=120, null=True)
    telefono = models.IntegerField(null=True)
    direccion = models.CharField(max_length=120, null=True)
    email = models.EmailField(null=True)
    notas = models.TextField(null=True)
    descripcion = models.TextField(null=True)
    web = models.URLField(null=True)
    fecha_alta = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre + ' ' + self.nif
    

class Proyecto(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    num_acuerdo = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empleados = models.ManyToManyField(Empleado)

    def __str__(self):
        return self.nombre 

class Tareas(models.Model):
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('muy_alta', 'Muy Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('muy_baja', 'Muy Baja')
    ]
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    empleado = models.ManyToManyField(Empleado)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    prioridad = models.CharField(max_length=120, choices=PRIORIDAD_CHOICES, default='media', null=True)

    def __str__(self):
        return self.nombre

