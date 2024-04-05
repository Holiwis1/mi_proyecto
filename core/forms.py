from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Empleado
from django.contrib.auth import get_user_model

User = get_user_model()

class EmpleadoSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'rol', 'telefono', 'fecha_nacimiento', 'direccion', 'num_seguridad_social', 'foto', 'foto_dni', 'fecha_alta')

        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'rol': 'Rol',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'direccion': 'Dirección',
            'num_seguridad_social': 'Número de seguridad social',
            'foto': 'Foto',
            'foto_dni': 'Foto del DNI',
            'fecha_alta': 'Fecha de alta'
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

        def __init__(self, *args, **kwargs):
            super(EmpleadoSignUpForm, self).__init__(*args, **kwargs)
            self.fields['email'].required = False
            self.fields['rol'].required = False
            self.fields['telefono'].required = False
            self.fields['fecha_nacimiento'].required = False
            self.fields['direccion'].required = False
            self.fields['num_seguridad_social'].required = False
            self.fields['foto'].required = False
            self.fields['foto_dni'].required = False
            self.fields['fecha_alta'].required = False