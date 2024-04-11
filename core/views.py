from multiprocessing import context
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from core.forms import ClienteForm, EmpleadoSignUpForm, EmpleadoCambiarFoto
from .models import Empleado, Cliente, Tareas, Proyecto
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render
from django.core.paginator import Paginator
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from django.db.models import Q

# mostrar la lista de empleados
def lista_empleados(request):
    # Obtener todos los empleados y ordenarlos por un campo (por ejemplo, id)
    empleados = Empleado.objects.order_by('id')

    # Obtener el nombre ingresado en el formulario de búsqueda
    nombre_busqueda = request.GET.get('search')

    # Filtrar empleados por nombre si se ingresó un valor en el formulario
    if nombre_busqueda:
        # Utilizando Q para hacer la consulta con OR lógico
        empleados = empleados.filter(
            Q(first_name__icontains=nombre_busqueda) |  # Buscar por primer nombre
            Q(last_name__icontains=nombre_busqueda)    # Buscar por apellido
        )

    # Crear un objeto Paginator con los empleados y mostrar 10 por página
    paginator = Paginator(empleados, 10)
    
    # Obtener el número de página desde la URL, por defecto es 1
    page_number = request.GET.get('page', 1)

    # Obtener la página actual
    page_obj = paginator.get_page(page_number)

    # Renderizar la plantilla con la página actual de empleados
    return render(request, 'core/lista_empleados.html', {'page_obj': page_obj})

#listado de clientes ordenado por id
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('id')
    paginator = Paginator(clientes, 2)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/lista_clientes.html', {'page_obj': page_obj})

#mostrar pagina indice
def indice(request):
    return render(request, 'core/indice.html')

#mostrar pagina home
def home(request):
    return render(request, 'core/home.html')

#ruta no encontrada errores
def handler404(request, exception):
    return render(request, 'core/error.html')

#registro de usuario/empleados
def registro_empleado(request):
    if request.method == 'POST':
        form = EmpleadoSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('lista_empleados')
        else:
            messages.error(request, 'Error al registrar el usuario')
    else:
        form = EmpleadoSignUpForm()
    return render(request, 'core/registro_empleado.html', {'form': form})

#mostrar el perfil de un empleado, con informacion como imagen, nombre, apellido, email, etc
def perfil_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, pk=empleado_id)

    if request.method == 'POST':
        form = EmpleadoCambiarFoto(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            form.save()
            # Aquí, puedes redirigir a alguna página, por ejemplo, la página de perfil del empleado.
            return redirect('perfil_empleado', empleado_id=empleado.id)
    else:
        # Inicializa el formulario con la instancia de 'empleado' para los casos GET.
        form = EmpleadoCambiarFoto(instance=empleado)
    return render(request, 'core/perfil_empleado.html', context={'empleado': empleado, 'form': form})


#Registrar un cliente
def registro_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_empleados')
    else:
        form = ClienteForm()
    
    return render(request, 'core/registro_cliente.html', {'form': form})
    

def descargar_pdf(request, empleado_id):
    empleado = Empleado.objects.get(pk=empleado_id)

    # Crear un archivo PDF en memoria
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Agregar imagen en el header
    header_image_path = 'https://navegatel.org/wp-content/uploads/2022/08/logo-navegatel-grande.webp'
    pdf.drawImage(header_image_path, 0, letter[1] - (0.5 * inch), width=letter[0], height=0.5 * inch, preserveAspectRatio=True, anchor='sw')

    # Agregar la primera imagen al PDF
    if empleado.foto_dni:
        image_data = ImageReader(empleado.foto_dni.path)
        pdf.drawImage(image_data, 150, 400, width=300, height=250)

    # Agregar la segunda imagen al PDF
    if empleado.foto_dni2:
        image_data2 = ImageReader(empleado.foto_dni2.path)
        pdf.drawImage(image_data2, 150, 100, width=300, height=250)

    pdf.setTitle(f"Foto DNI - {empleado.get_full_name()}")
    pdf.showPage()
    pdf.save()

    # Configurar la respuesta para descargar el PDF
    buffer.seek(0)
    response = FileResponse(buffer, as_attachment=True, filename=f"foto_dni_{empleado.get_full_name()}.pdf")
    return response

#Eliminar empleado, recibo su id, elimino y refresco pagina
def eliminar_empleado(request, empleado_id):
    empleado = Empleado.objects.get(pk=empleado_id)
    empleado.delete()
    return redirect('lista_empleados')

#Editar información de empleado
def editar_empleado(request, empleado_id):
    empleado = Empleado.objects.get(pk=empleado_id)
    if request.method == 'POST':
        form = EmpleadoSignUpForm(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('lista_empleados')
    else:
        form = EmpleadoSignUpForm(instance=empleado)
    return render(request, 'core/editar_empleado.html', {'form': form})