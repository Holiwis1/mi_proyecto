from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from core.forms import ClienteForm, EmpleadoSignUpForm
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

def perfil_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, pk=empleado_id)

    context = {
        'empleado': empleado
    }

    return render(request, 'core/perfil_empleado.html', context)

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
