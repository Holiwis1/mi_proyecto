from functools import wraps
import json
from multiprocessing import context
import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from core.forms import ClienteEditarForm, ClienteForm, EmpleadoSignUpForm, EmpleadoCambiarFoto, EmpleadoEditarForm, ProyectoForm,TicketAttachmentForm, TableForm, TareaForm, TicketForm
from mi_proyecto import settings
from .models import Empleado, Cliente, Tareas, Proyecto, Table, Ticket, Archivo, TicketAttachment
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render
from django.core.paginator import Paginator
import io
from .decorators import admin_required
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

# ********************************************** EMPLEADOS****************************************************
# Mostrar la lista de empleados
@login_required
@admin_required
def lista_empleados(request):
    """
    Muestra una lista de empleados con opciones de búsqueda y paginación.
    """
    empleados = Empleado.objects.order_by('id')
    nombre_busqueda = request.GET.get('search')

    # Filtrar empleados por el término de búsqueda
    if nombre_busqueda:
        empleados = empleados.filter(
            Q(first_name__icontains=nombre_busqueda) |  # Primer nombre
            Q(last_name__icontains=nombre_busqueda) |   # Apellido
            Q(rol__icontains=nombre_busqueda) |         # Rol
            Q(telefono__icontains=nombre_busqueda) |    # Teléfono
            Q(fecha_nacimiento__icontains=nombre_busqueda) |  # Fecha de nacimiento
            Q(direccion__icontains=nombre_busqueda) |   # Dirección
            Q(num_seguridad_social__icontains=nombre_busqueda) | # Número de seguridad social
            Q(fecha_alta__icontains=nombre_busqueda) | # Fecha de alta
            Q(email__icontains=nombre_busqueda) |      # Email
            Q(username__icontains=nombre_busqueda)     # Nombre de usuario
        )

    paginator = Paginator(empleados, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/lista_empleados.html', {'page_obj': page_obj})



#registro de usuario/empleados
def registro_empleado(request):
    """
    Registra un nuevo empleado.
    """
    if request.method == 'POST':
        form = EmpleadoSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Error al registrar el usuario')
    else:
        form = EmpleadoSignUpForm()
    return render(request, 'core/registro_empleado.html', {'form': form})



#mostrar el perfil de un empleado, con informacion como imagen, nombre, apellido, email, etc
@login_required
def perfil_empleado(request, empleado_id):
    """
    Muestra el perfil de un empleado con opción de cambiar la foto.
    """
    empleado = get_object_or_404(Empleado, pk=empleado_id)

    if request.method == 'POST':
        form = EmpleadoCambiarFoto(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('perfil_empleado', empleado_id=empleado.id)
    else:
        form = EmpleadoCambiarFoto(instance=empleado)

    profile_image_url = empleado.foto.url if empleado.foto else None

    return render(request, 'core/perfil_empleado.html', context={'empleado': empleado, 'form': form, 'profile_image_url': profile_image_url})

#Descargar PDF con la foto del DNI de un empleado
@login_required
def descargar_pdf(request, empleado_id):
    """
    Descarga un PDF con la foto del DNI de un empleado.
    """
    empleado = Empleado.objects.get(pk=empleado_id)
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Agregar imagen en el header
    header_image_path = 'https://navegatel.org/wp-content/uploads/2022/08/logo-navegatel-grande.webp'
    pdf.drawImage(header_image_path, 0, letter[1] - (0.5 * inch), width=letter[0], height=0.5 * inch, preserveAspectRatio=True, anchor='sw')

    # Agregar imágenes del DNI al PDF
    if empleado.foto_dni:
        image_data = ImageReader(empleado.foto_dni.path)
        pdf.drawImage(image_data, 150, 400, width=300, height=250)
    if empleado.foto_dni2:
        image_data2 = ImageReader(empleado.foto_dni2.path)
        pdf.drawImage(image_data2, 150, 100, width=300, height=250)

    pdf.setTitle(f"Foto DNI - {empleado.get_full_name()}")
    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    response = FileResponse(buffer, as_attachment=True, filename=f"foto_dni_{empleado.get_full_name()}.pdf")
    return response

#Eliminar empleado, recibo su id, elimino y refresco pagina
@login_required
@admin_required
def eliminar_empleado(request, empleado_id):
    """
    Elimina un empleado.
    """
    empleado = Empleado.objects.get(pk=empleado_id)
    empleado.delete()
    return redirect('lista_empleados')


#Editar información de empleado
@login_required
@admin_required
def editar_empleado(request, empleado_id):
    """
    Edita la información de un empleado.
    """
    empleado = get_object_or_404(Empleado, pk=empleado_id)
    if request.method == 'POST':
        form = EmpleadoEditarForm(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('lista_empleados')
    else:
        form = EmpleadoEditarForm(instance=empleado)
    
    return render(request, 'core/editar_empleado.html', {'form': form})





#listado de clientes ordenado por id
@login_required
@admin_required
def lista_clientes(request):
    """
    Muestra una lista de clientes con opciones de búsqueda y paginación.
    """
    clientes = Cliente.objects.order_by('id')
    cliente_busqueda = request.GET.get('search')

    if cliente_busqueda:
        clientes = clientes.filter(
            Q(nombre__icontains=cliente_busqueda) |          # Nombre
            Q(nombre_comercial__icontains=cliente_busqueda) | # Nombre comercial
            Q(nif__icontains=cliente_busqueda) |             # NIF
            Q(razon_social__icontains=cliente_busqueda) |    # Razón social
            Q(tipo__icontains=cliente_busqueda) |            # Tipo
            Q(telefono__icontains=cliente_busqueda) |        # Teléfono
            Q(direccion__icontains=cliente_busqueda) |       # Dirección
            Q(email__icontains=cliente_busqueda) |           # Email
            Q(notas__icontains=cliente_busqueda) |           # Notas
            Q(descripcion__icontains=cliente_busqueda) |     # Descripción
            Q(web__icontains=cliente_busqueda) |             # Web
            Q(telefono2__icontains=cliente_busqueda)         # Segundo teléfono
        )

    paginator = Paginator(clientes, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/lista_clientes.html', {'page_obj': page_obj})



#*************************************ERRORES*****************************
#ruta no encontrada errores
def handler404(request, exception):
    """
    Muestra una página de error personalizada.
    """
    return render(request, 'core/error.html')



#Registrar un cliente
@login_required
@admin_required
def registro_cliente(request):
    """
    Registra un nuevo cliente.
    """
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_empleados')
    else:
        form = ClienteForm()
    
    return render(request, 'core/registro_cliente.html', {'form': form})
    

# ********************************************** CLIENTES****************************************************

#Editar información de cliente
@login_required
@admin_required
def editar_cliente(request, cliente_id):
    """
    Edita la información de un cliente.
    """
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
@login_required
@admin_required
def eliminar_cliente(request, cliente_id):
    """
    Elimina un cliente.
    """
    cliente = Cliente.objects.get(pk=cliente_id)
    cliente.delete()
    return redirect('lista_clientes')


#perfil cliente 
@login_required
@admin_required
def perfil_cliente(request, cliente_id):
    """
    Muestra el perfil de un cliente.
    """
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'core/perfil_cliente.html', {'cliente': cliente})

#Descargar archivos
@login_required
def descargar_archivos(request, archivo_id):
    """
    Descarga un archivo asociado a un cliente.
    """
    archivo = get_object_or_404(Archivo, id=archivo_id)
    file_path = archivo.archivo.path
    return FileResponse(open(file_path, 'rb'))

#guardar archivos
@login_required
def guardar_archivos(request):
    """
    Guarda archivos asociados a un cliente.
    """
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        files = request.FILES.getlist('files[]')

        try:
            cliente = Cliente.objects.get(pk=cliente_id)
        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

        for file in files:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            Archivo.objects.create(cliente=cliente, archivo=filename)

        archivos_cliente = cliente.archivos.all()
        archivos_info = [{'name': archivo.archivo.name, 'url': archivo.archivo.url} for archivo in archivos_cliente]

        return JsonResponse({'files': archivos_info})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

#Editar nombre archivo
@login_required
def cambiar_nombre_archivo(request, archivo_id):
    if request.method == 'POST':
        nuevo_nombre = request.POST.get('nuevo_nombre', None)
        if not nuevo_nombre:
            return JsonResponse({'error': 'No se proporcionó un nuevo nombre'}, status=400)

        archivo = get_object_or_404(Archivo, id=archivo_id)
        cliente_id = archivo.cliente.id

        # Obtener la extensión del archivo original
        base_name, ext = os.path.splitext(archivo.archivo.name)

        # Crear el nuevo nombre usando la base proporcionada y la extensión original
        nuevo_nombre_path = f'{nuevo_nombre}{ext}'

        # Rutas del archivo original y nuevo
        old_path = os.path.join(settings.MEDIA_ROOT, archivo.archivo.name)
        new_path = os.path.join(settings.MEDIA_ROOT, nuevo_nombre_path)

        # Verificar si el directorio de destino existe, si no, crearlo
        new_dir = os.path.dirname(new_path)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

        # Renombrar el archivo físico si el original existe
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
        else:
            return JsonResponse({'error': 'El archivo original no existe'}, status=404)

        # Actualizar el campo del archivo en el modelo
        archivo.archivo.name = nuevo_nombre_path
        archivo.save()

        return redirect('perfil_cliente', cliente_id=cliente_id)  # Redirigir a la misma página

    return JsonResponse({'error': 'Método no permitido'}, status=405)


#Eliminar archivo
@login_required
def eliminar_archivo(request, archivo_id):
    if request.method == 'POST':
        archivo = get_object_or_404(Archivo, id=archivo_id)

        # Obtener el cliente al que pertenece el archivo
        cliente_id = archivo.cliente.id
        
        # Eliminar el archivo del sistema de archivos
        archivo.archivo.delete()  
        
        # Eliminar el objeto del modelo
        archivo.delete()  
        
        # Redirigir a la página del perfil
        return redirect('perfil_cliente', cliente_id=cliente_id)  # Redirigir a la misma página

    return HttpResponse("Método no permitido", status=405)


# ********************************************** TRELLO ****************************************************
@csrf_exempt
def mover_tabla(request, table_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_position = data.get('new_position')

        table = get_object_or_404(Table, id=table_id)
        tables = list(Table.objects.all())

        # Remove the table from its current position
        tables.remove(table)
        # Insert the table at the new position
        tables.insert(new_position, table)

        # Update the position for each table in the new list
        for index, table in enumerate(tables):
            table.position = index
            table.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail'}, status=400)


@login_required
def crear_tabla(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        
        if form.is_valid():
            table = form.save()
            # Redirecciona al perfil del empleado después de guardar la tabla
            return redirect('index') 
    else:
        form = TableForm()
    
    tables = Table.objects.all()
    return render(request, 'core/index.html', {'form': form, 'tables': tables})

@login_required
def index(request):
    tables = Table.objects.all()
    tickets = Ticket.objects.all()  # Obtener todos los tickets
    
    return render(request, 'core/index.html', {'tables': tables, 'tickets': tickets})

@login_required
def table_detail(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    tickets = Ticket.objects.filter(table=table)
    return render(request, 'core/table_detail.html', {'table': table, 'tickets': tickets})

@login_required
def ticket_create(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        attachment_form = TicketAttachmentForm(request.POST, request.FILES)
        
        if ticket_form.is_valid() and attachment_form.is_valid():
            # Guardar el formulario del ticket
            ticket = ticket_form.save(commit=False)
            ticket.table = table
            ticket.save()

            # Guardar el formulario del archivo adjunto
            attachment = attachment_form.save(commit=False)
            attachment.ticket = ticket  # Asociar el archivo adjunto con el ticket
            attachment.save()

            return redirect('index')
    else:
        ticket_form = TicketForm()
        attachment_form = TicketAttachmentForm()
    
    return render(request, 'core/ticket_form.html', {'ticket_form': ticket_form, 'attachment_form': attachment_form})

@login_required
def upload_attachment(request):
    if request.method == 'POST':
        form = TicketAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirige a donde desees después de cargar el archivo
    else:
        form = TicketAttachmentForm()
    return render(request, 'upload_attachment.html', {'form': form})

#Actualizar ticket 
@login_required
def ticket_update(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, instance=ticket)
        if ticket_form.is_valid():
            # Guardar el formulario del ticket actualizado
            ticket = ticket_form.save()

            # Guardar los archivos adjuntos
            files = request.FILES.getlist('file')
            for file in files:
                # Verificar si el archivo ya existe en la base de datos para evitar duplicados
                if not TicketAttachment.objects.filter(ticket=ticket, file=file.name).exists():
                    attachment = TicketAttachment(ticket=ticket, file=file)
                    attachment.save()

            return redirect('index')
    else:
        ticket_form = TicketForm(instance=ticket)  # Pasar la instancia del ticket al formulario
        attachments = TicketAttachment.objects.filter(ticket=ticket)
        attachment_form = TicketAttachmentForm()  # Formulario para nuevos archivos adjuntos

    return render(request, 'core/ticket_form.html', {
        'ticket_form': ticket_form,
        'attachment_form': attachment_form,
        'attachments': attachments
    })


@login_required
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket.delete()
    return redirect('index')

@login_required
def eliminar_tabla(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    table.delete()
    return JsonResponse({'message': 'Tabla eliminada exitosamente'})

"""@login_required
def crear_etiqueta(request):
    if request.method == 'POST':
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('url_de_redireccion')
    else:
        form = EtiquetaForm()
    return render(request, 'crear_etiqueta.html', {'form': form})"""
@login_required
def mover_ticket(request, ticket_id, table_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    nueva_tabla = get_object_or_404(Table, pk=table_id)
    
    if request.method == 'POST':
        ticket.table = nueva_tabla
        ticket.save()
        return JsonResponse({'status': 'ok'})
    
    return JsonResponse({'status': 'error'}, status=400)
def update_table_color(request, table_id):
    if request.method == 'POST':
        table = get_object_or_404(Table, id=table_id)
        data = json.loads(request.body)
        table.header_color = data.get('color', '#ffffff')
        table.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

def my_view(request):
    return render(request, 'core/index.html')

# ********************************************** PROYECTOS****************************************************
#Crear proyectos
@login_required
@admin_required
def crear_proyecto(request):
    empleados = Empleado.objects.all()
    clientes = Cliente.objects.all()
    context = {
        'empleados': empleados,
        'clientes': clientes,  
        'PRIORIDAD_CHOICES': Proyecto.PRIORIDAD_CHOICES,
        'ESTADOS_CHOICES': Proyecto.ESTADOS_CHOICES,
        'TIPO_CHOICES': Proyecto.TIPO_CHOICES
    }

    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.save()
            # Guarda las relaciones ManyToMany para empleados
            proyecto.empleados.set(form.cleaned_data['empleados'])
            return redirect('lista_proyectos')  # Ajusta según la redirección deseada
    else:
        form = ProyectoForm()

    context['form'] = form
    return render(request, 'core/crear_proyecto.html', context)

@login_required
@admin_required
def lista_proyectos(request):
    """
    Muestra una lista de proyectos con opciones de búsqueda y paginación.
    """
    proyecto_list = Proyecto.objects.all()
    proyecto_busqueda = request.GET.get('search')

    if proyecto_busqueda:
        proyecto_list = proyecto_list.filter(
            Q(nombre__icontains=proyecto_busqueda) |
            Q(descripcion__icontains=proyecto_busqueda) |
            Q(cliente__nombre__icontains=proyecto_busqueda) |
            Q(tipo__icontains=proyecto_busqueda)
        )

    paginator = Paginator(proyecto_list, 10)  # Mostrar 10 proyectos por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/proyectos.html', {'page_obj': page_obj, 'proyectos': page_obj.object_list})
   


#Editar un proyecto
@login_required
@admin_required
def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.save()
            # Actualiza los empleados seleccionados en la relación ManyToMany
            empleados_ids = request.POST.getlist('empleados')
            proyecto.empleados.set(empleados_ids)
            return redirect('lista_proyectos')
    else:
        form = ProyectoForm(instance=proyecto)

    empleados = Empleado.objects.all()
    clientes = Cliente.objects.all()
    empleados_seleccionados = proyecto.empleados.values_list('id', flat=True)
    context = {
        'form': form,
        'proyecto': proyecto,
        'empleados': empleados,
        'clientes': clientes,
        'PRIORIDAD_CHOICES': Proyecto.PRIORIDAD_CHOICES,
        'ESTADOS_CHOICES': Proyecto.ESTADOS_CHOICES,
        'TIPO_CHOICES': Proyecto.TIPO_CHOICES,
        'empleados_seleccionados': list(empleados_seleccionados)
    }
    return render(request, 'core/editar_proyecto.html', context)

#Eliminar un proyecto
@login_required
@admin_required
def eliminar_proyecto(request, proyecto_id):
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    proyecto.delete()
    return redirect('lista_proyectos')

#*************************************************** TAREAS ********************************************************#
#Crear tareas
@login_required
@admin_required
def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tareas')  # Cambia 'lista_tareas' por la URL que prefieras para redirigir después de crear una tarea
    else:
        form = TareaForm()

    context = {
        'form': form,
        'proyectos': Proyecto.objects.all(),
        'empleados': Empleado.objects.all(),
        'clientes': Cliente.objects.all(),
        'PRIORIDAD_CHOICES': Tareas.PRIORIDAD_CHOICES,
        'ESTADOS_CHOICES': Tareas.ESTADOS_CHOICES,
    }
    return render(request, 'core/crear_tarea.html', context)

#Mostrar listado de tareas
@login_required
@admin_required
def lista_tareas(request):
    """
    Muestra una lista de tareas con opciones de búsqueda y paginación.
    """
    tareas = Tareas.objects.order_by('id')
    tarea_busqueda = request.GET.get('search')

    if tarea_busqueda:
        tareas = tareas.filter(
            Q(nombre__icontains=tarea_busqueda) |
            Q(descripcion__icontains=tarea_busqueda) |
            Q(proyecto__nombre__icontains=tarea_busqueda) |
            Q(cliente__nombre__icontains=tarea_busqueda) |
            Q(empleado__first_name__icontains=tarea_busqueda) |
            Q(empleado__last_name__icontains=tarea_busqueda)
        )

    paginator = Paginator(tareas, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/lista_tareas.html', {'page_obj': page_obj})

#Editar TAREAS
@login_required
@admin_required
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('lista_tareas')
    else:
        form = TareaForm(instance=tarea)

    context = {
        'form': form,
        'proyectos': Proyecto.objects.all(),
        'empleados': Empleado.objects.all(),
        'clientes': Cliente.objects.all(),
        'PRIORIDAD_CHOICES': Tareas.PRIORIDAD_CHOICES,
        'ESTADOS_CHOICES': Tareas.ESTADOS_CHOICES,
    }
    return render(request, 'core/editar_tarea.html', context)

#Eliminar tarea
@login_required
@admin_required
def eliminar_tarea(request,tarea_id):
    tarea = Tareas.objects.get(pk=tarea_id)
    tarea.delete()
    return redirect('lista_tareas')
