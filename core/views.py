from multiprocessing import context
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from core.forms import ClienteEditarForm, ClienteForm, EmpleadoSignUpForm, EmpleadoCambiarFoto, EmpleadoEditarForm
from .models import Empleado, Cliente, Tareas, Proyecto, Table, Ticket
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
from .forms import TableForm, TicketForm



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
            Q(last_name__icontains=nombre_busqueda) |   # Buscar por apellido
            Q(rol__icontains=nombre_busqueda) |         # Buscar por rol
            Q(telefono__icontains=nombre_busqueda) |    # Buscar por teléfono
            Q(fecha_nacimiento__icontains=nombre_busqueda) |  # Buscar por fecha de nacimiento
            Q(direccion__icontains=nombre_busqueda) |   # Buscar por dirección
            Q(num_seguridad_social__icontains=nombre_busqueda) | # Buscar por número de seguridad social
            Q(fecha_alta__icontains=nombre_busqueda) | # Buscar por fecha de alta
            Q(email__icontains=nombre_busqueda) | # Buscar por email
            Q(username__icontains=nombre_busqueda)  # Buscar por nombre completo (primer nombre + apellido)
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
    #Ordenar clientes por id
    clientes = Cliente.objects.all().order_by('id')
    
    #Obtener el nombre ingresado en el formulario de búsqueda
    cliente_busqueda = request.GET.get('search')
    
    #Filtracion de clientes por lo que se ingrese
    if cliente_busqueda:
        clientes = clientes.filter(
            Q(nombre__icontains=cliente_busqueda) |  # Buscar por nombre
            Q(nombre_comercial__icontains=cliente_busqueda) |   # Buscar por nombre comercial
            Q(nif__icontains=cliente_busqueda) |   # Buscar por NIF
            Q(razon_social__icontains=cliente_busqueda) |   # Buscar por razón social
            Q(tipo__icontains=cliente_busqueda) |   # Buscar por tipo
            Q(telefono__icontains=cliente_busqueda) |   # Buscar por teléfono
            Q(direccion__icontains=cliente_busqueda) |   # Buscar por dirección
            Q(email__icontains=cliente_busqueda) |   # Buscar por email
            Q(notas__icontains=cliente_busqueda) |   # Buscar por notas
            Q(descripcion__icontains=cliente_busqueda) |   # Buscar por descripción
            Q(web__icontains=cliente_busqueda) |  # Buscar por web
            Q(telefono2__icontains=cliente_busqueda)  # Buscar por segundo teléfono
        )

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
    


#Descargar PDF con la foto del DNI de un empleado
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
    empleado = get_object_or_404(Empleado, pk=empleado_id)
    if request.method == 'POST':
        form = EmpleadoEditarForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado actualizado con éxito.')
            return redirect('lista_empleados')  # Asume que tienes una URL nombrada 'lista_empleados'
    else:
        form = EmpleadoEditarForm(instance=empleado)
    
    return render(request, 'core/editar_empleado.html', {'form': form})


#Editar información de cliente
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        form = ClienteEditarForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado con éxito.')
            return redirect('lista_clientes')  
    else:
        form = ClienteEditarForm(instance=cliente)
    
    return render(request, 'core/editar_cliente.html', {'form': form})



#Eliminar cliente, recibo su id, elimino y refresco pagina
def eliminar_cliente(request, cliente_id):
    cliente = Cliente.objects.get(pk=cliente_id)
    cliente.delete()
    return redirect('lista_clientes')

#perfil cliente 
def perfil_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'core/perfil_cliente.html', {'cliente': cliente})

 #TRELLO

def crear_tabla(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('table_list') 
    else:
        form = TableForm()
    
    tables = Table.objects.all()
    return render(request, 'core/table_list.html', {'form': form, 'tables': tables})
def table_list(request):
    tables = Table.objects.all()
    return render(request, 'core/table_list.html', {'tables': tables})

def table_detail(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    tickets = Ticket.objects.filter(table=table)
    return render(request, 'core/table_detail.html', {'table': table, 'tickets': tickets})

def ticket_create(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.table = table
            ticket.save()
            return redirect('table_list') 
    else:
        form = TicketForm()
    return render(request, 'core/ticket_form.html', {'form': form})

def ticket_update(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('table_list', table_id=ticket.table.id)
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'core/ticket_form.html', {'form': form})

def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    table_id = ticket.table.id
    ticket.delete()
    return redirect('table_list', table_id=table_id)

def eliminar_tabla(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    table.delete()
    return JsonResponse({'message': 'Tabla eliminada exitosamente'})