from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Cliente, Table, Ticket,Empleado, TicketAttachment
#****************************** USUARIO ******************************#
User = get_user_model()
#****************************** EMPLEADO ******************************#
class EmpleadoSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'rol', 'telefono', 'telefono2', 'fecha_nacimiento', 'direccion', 'num_seguridad_social', 'foto', 'foto_dni','foto_dni', 'foto_dni2', 'fecha_alta')

        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'telefono2': 'Móvil', 
            'rol': 'Rol',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'direccion': 'Dirección',
            'num_seguridad_social': 'Número de seguridad social',
            'foto': 'Foto',
            'foto_dni': 'Foto del por delante',
            'foto_dni2': 'Foto del dni por detras',
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



            
#Modelo para cambiar la foto de perfil del empleado desde su propio perfil
class EmpleadoCambiarFoto(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['foto'] #Cambiar la foto de perfil


#Modelo para cambiar cualquier campo del empleado
class EmpleadoEditarForm(forms.ModelForm):

    new_password = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(label='Repetir nueva contraseña', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'rol', 'telefono','telefono2', 'fecha_nacimiento', 'direccion', 'num_seguridad_social', 'foto_dni', 'foto_dni2', 'fecha_alta')
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'telefono2': 'Móvil',
            'rol': 'Rol',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'direccion': 'Dirección',
            'num_seguridad_social': 'Número de seguridad social',
            'foto_dni': 'Foto del DNI por delante',
            'foto_dni2': 'Foto del DNI por detrás',
            'fecha_alta': 'Fecha de alta'
        }

    def __init__(self, *args, **kwargs):
        super(EmpleadoEditarForm, self).__init__(*args, **kwargs)
        # Ajustar la obligatoriedad de los campos según sea necesario
        self.fields['email'].required = False
        self.fields['rol'].required = False
        self.fields['telefono'].required = False
        self.fields['fecha_nacimiento'].required = False
        self.fields['direccion'].required = False
        self.fields['num_seguridad_social'].required = False
        self.fields['foto_dni'].required = False
        self.fields['foto_dni2'].required = False
        self.fields['fecha_alta'].required = False
        self.fields['telefono2'].required = False

        
#****************************** CLIENTES ******************************#

# Cambiarlo y dejarlo como arriba para poder editar en html
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'  #O lista los campos que deseas incluir en el formulario



    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password1 != password2:
            self.add_error('new_password2', "Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("new_password1"):
            user.set_password(self.cleaned_data["new_password1"])
        if commit:
            user.save()
        return user


#Modelo para cambiar cualquier campo del cliente
class ClienteEditarForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nombre', 'nombre_comercial', 'nif', 'tipo', 'razon_social', 'telefono', 'telefono2', 'direccion', 'email', 'notas', 'descripcion', 'web')
        labels = {
            'nombre': 'Nombre',
            'nombre_comercial': 'Nombre Comercial',
            'nif': 'NIF',
            'tipo': 'Tipo',
            'razon_social': 'Razón Social',
            'telefono': 'Teléfono',
            'telefono2': 'Móvil',
            'direccion': 'Dirección',
            'email': 'Correo electrónico',
            'notas': 'Notas',
            'descripcion': 'Descripción',
            'web': 'Web'
        }

    def __init__(self, *args, **kwargs):
        super(ClienteEditarForm, self).__init__(*args, **kwargs)
        # Ajustar la obligatoriedad de los campos según sea necesario
        self.fields['nombre_comercial'].required = False
        self.fields['telefono'].required = False
        self.fields['telefono2'].required = False
        self.fields['direccion'].required = False
        self.fields['nif'].required = False
        self.fields['tipo'].required = False
        self.fields['razon_social'].required = False
        self.fields['email'].required = False
        self.fields['notas'].required = False
        self.fields['descripcion'].required = False
        self.fields['web'].required = False

    
#****************************** TRELLO ******************************#
class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['name']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']
        
class TicketAttachmentForm(forms.ModelForm):
    class Meta:
        model = TicketAttachment
        fields = ['file']