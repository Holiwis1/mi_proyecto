from django.shortcuts import render, redirect, get_object_or_404
from core.forms import EmpleadoSignUpForm
from .models import Empleado, Cliente, Tareas, Proyecto
from django.contrib.auth import login
from django.shortcuts import render
from django.core.paginator import Paginator


# mostrar la lista de empleados
def lista_empleados(request):
    # Obtener todos los empleados y ordenarlos por un campo (por ejemplo, id)
    empleados = Empleado.objects.order_by('id')

    # Crear un objeto Paginator con los empleados y mostrar 10 por página
    paginator = Paginator(empleados, 10)
    
    # Obtener el número de página desde la URL, por defecto es 1
    page_number = request.GET.get('page', 1)

    # Obtener la página actual
    page_obj = paginator.get_page(page_number)

    # Renderizar la plantilla con la página actual de empleados
    return render(request, 'core/lista_empleados.html', {'page_obj': page_obj})


def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('id')
    paginator = Paginator(clientes, 2)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/lista_clientes.html', {'page_obj': page_obj})

#mostrar pagina indice
def indice(request):
    return render(request, 'core/indice.html')

def home(request):
    return render(request, 'core/home.html')
#ruta no encontrada errores
def handler404(request, exception):
    return render(request, 'core/error.html')

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

def perfil_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, pk=empleado_id)

    context = {
        'empleado': empleado
    }

    return render(request, 'core/perfil_empleado.html', context)

def registro_empleados(request):
    if request.method == 'POST':
        form = EmpleadoSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('indice')
    else:
        form = EmpleadoSignUpForm()
    return render(request, 'core/registro_empleados.html', {'form': form})

