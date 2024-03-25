from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Empleado, Cliente, Tareas, Proyecto

# Registro de los modelos en la site de admin
admin.site.register(Empleado, UserAdmin)
admin.site.register(Cliente)
admin.site.register(Tareas)
admin.site.register(Proyecto)