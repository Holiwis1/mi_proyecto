# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

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
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=120, null=True, blank=True)
    num_seguridad_social = models.IntegerField(null=True, blank=True)
    telefono2 = models.IntegerField(null=True, blank=True)
    foto = models.ImageField(upload_to='images/', null=True, blank=True)
    foto_dni = models.ImageField(upload_to='dnis/', null=True, blank=True)
    foto_dni2 = models.ImageField(upload_to='dnis/', null=True, blank=True)
    fecha_alta = models.DateField(blank=True, null=True)

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
    nombre_comercial = models.CharField(max_length=120, null=True, blank=True)
    nif = models.CharField(max_length=9, null=True, blank=True)
    tipo = models.CharField(max_length=120, choices=TIPO_CHOICES, default='empresa', null=True, blank=True)
    razon_social = models.CharField(max_length=120, null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    telefono2 = models.IntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    web = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.nombre + ' ' + self.nif
    

class Proyecto(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    num_acuerdo = models.IntegerField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    empleados = models.ManyToManyField(Empleado)

    def __str__(self):
        return self.nombre 

class Tareas(models.Model):
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('muy_alta', 'Muy Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('muy_baja', 'Muy Baja'),
        ('sin_prioridad', 'Sin Prioridad')
    ]
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    empleado = models.ManyToManyField(Empleado)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True, blank=True)
    prioridad = models.CharField(max_length=120, choices=PRIORIDAD_CHOICES, default='sin_prioridad', null=True, blank=True)

    def __str__(self):
        return self.nombre
        
class Table(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    table = models.ForeignKey(Table, related_name='tickets', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  # Campo auto-completado

    def __str__(self):
        return self.title