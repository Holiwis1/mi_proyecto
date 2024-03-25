from django.shortcuts import render, redirect
from core.forms import EmpleadoSignUpForm
from .models import Empleado, Cliente, Tareas, Proyecto
from django.contrib.auth import login

# mostrar la lista de empleados
def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'core/lista_empleados.html', {'empleados': empleados})

#mostrar pagina indice
def indice(request):
    return render(request, 'core/indice.html')

def home(request):
    return render(request, 'core/home.html')

#registro de usuario/empleados
def registro_empleado(request):
    if request.method == 'POST':
        form = EmpleadoSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('empleados')
    else:
        form = EmpleadoSignUpForm()
    return render(request, 'core/registro_empleado.html', {'form': form})