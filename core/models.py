# Create your models here.
from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


#****************************** EMPLEADO ******************************#

#****************************** MODELO EMPLEADO ******************************#
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


#****************************** CLIENTE ******************************#

#****************************** MODELO CLIENTE ******************************#
class Cliente(models.Model):
    # Opciones de tipo de cliente
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
        



#****************************** PROYECTO ******************************#

#****************************** MODELO PROYECTO ******************************#
class Proyecto(models.Model):
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('muy_alta', 'Muy Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('muy_baja', 'Muy Baja'),
        ('sin_prioridad', 'Sin Prioridad')
    ]
    ESTADOS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('activo', 'Activo'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
        ('permanente', 'Permanente')
    ]
    TIPO_CHOICES = [
        ('1ª Justificacion', '1ª Justificacion'),
        ('2ª Justificacion', '2ª Justificacion'),
        ('Acuerdos', 'Acuerdos'),
        ('Diseño Gráfico', 'Diseño Gráfico'),
        ('E-Commerce', 'E-Commerce'),
        ('Factura electrónica', 'Factura electrónica'),
        ('Gestión Clientes', 'Gestión Clientes'),
        ('Gestión Procesos', 'Gestión Procesos'),
        ('Kit Digital', 'Kit Digital'),
        ('Marketing', 'Marketing'),
        ('Solicitud KD', 'Solicitud KD'),
        ('Redes Sociales', 'Redes Sociales'),
        ('SEO', 'SEO'),
        ('Web', 'Web'), 
        ('TPV', 'TPV'), 
        ('Diseño Gráfico', 'Diseño Gráfico'),
        ('URL', 'URL')
    ]
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    num_acuerdo = models.IntegerField(null=True, blank=True)
    prioridad = models.CharField(max_length=120, choices=PRIORIDAD_CHOICES, default='sin_prioridad', null=True, blank=True)
    estado = models.CharField(max_length=120, choices=ESTADOS_CHOICES, default='pendiente', null=True, blank=True)
    valor = models.IntegerField(null=True, blank=True)
    tipo = models.CharField(max_length=120, choices=TIPO_CHOICES, null=True, blank=True)
    firma_acuerdo = models.DateField(null=True, blank=True)
    fecha_facturacion = models.DateField(null=True, blank=True)
    num_factura = models.IntegerField(null=True, blank=True)
    fecha_cobro_IVA = models.DateField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    empleados = models.ManyToManyField(Empleado)

    def __str__(self):
        return self.nombre 

#****************************** TAREAS ******************************#

#****************************** MODELO TAREAS ******************************#
class Tareas(models.Model):
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('muy_alta', 'Muy Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('muy_baja', 'Muy Baja'),
        ('sin_prioridad', 'Sin Prioridad')
    ]
    ESTADOS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('activo', 'Activo'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
        ('permanente', 'Permanente')
    ]
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True, blank=True)
    prioridad = models.CharField(max_length=120, choices=PRIORIDAD_CHOICES, default='sin_prioridad', null=True, blank=True)
    estado = models.CharField(max_length=120, choices=ESTADOS_CHOICES, default='pendiente', null=True, blank=True)
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
#****************************** NOTAS ******************************#
class Notas(models.Model):
    titulo = models.CharField(max_length=120)
    descripcion = models.TextField(null=True, blank=True)
    fecha_creación = models.DateField(auto_now_add=True, null=True, blank=True, editable=False)
    fecha_editado = models.DateField(auto_now=True, null=True, blank=True, editable=False)

    def __str__(self):
        return self.titulo
    
#****************************** TRELLO ******************************#
        
#****************************** MODELO TABLA ******************************#
class Table(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#****************************** MODELO TICKETS ******************************#
class Ticket(models.Model):
    table = models.ForeignKey(Table, related_name='tickets', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  # Campo auto-completado

    def __str__(self):
        return self.title


#****************************** MODELO ARCHIVOS_TICKETS ******************************#
class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='ticket_attachments/')
    
#****************************** MODELO ARCHIVO ******************************#
#Clase archivo para poder subir cualquier numero de archivos al cliente
class Archivo(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='archivos', on_delete=models.CASCADE, null=True, blank=True)
    archivo = models.FileField(upload_to='archivos_clientes/')
    name = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    Proyecto = models.ForeignKey(Proyecto, related_name='archivos', on_delete=models.CASCADE, null=True, blank=True)
    Tareas = models.ForeignKey(Tareas, related_name='archivos', on_delete=models.CASCADE, null=True, blank=True)
    tickets = models.ForeignKey(Ticket, related_name='archivos', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Si el objeto es nuevo (no tiene ID), asigna la descripción y el nombre
        if not self.pk:  # Esto verifica si el objeto ya existe
            self.descripcion = str(self.archivo)  # Solo se asigna al crear
        self.name = str(self.archivo)  # Asigna el nombre del archivo cuando quiera, ya que se puede editar
        super().save(*args, **kwargs)  # Llama a la función save original


#****************************** MODELO ETIQUETAS ******************************#
class Etiqueta(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name