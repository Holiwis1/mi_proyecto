from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Empleado

class EmpleadoSignUpForm(UserCreationForm):
    class Meta:
        model = Empleado
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'rol','password']

        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'rol': 'Rol',
            'password': 'Contraseña',
            
        }
        error_messages = {
            'username': {
                'unique': 'El nombre de usuario ya existe',
                'max_length': 'El nombre de usuario es muy largo',
                'required': 'Campo requerido'
            }
        }
        help_texts = {
            'username': None,
        }