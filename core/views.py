from functools import wraps
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


# Mostrar la lista de empleados
@login_required
@admin_required
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
@login_required
@admin_required
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

    paginator = Paginator(clientes, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/lista_clientes.html', {'page_obj': page_obj})



#mostrar pagina indice
@login_required
def indice(request):
    return render(request, 'table_list')


#ruta no encontrada errores
def handler404(request, exception):
    return render(request, 'core/error.html')


#registro de usuario/empleados
@login_required
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
@login_required
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

    # Obtener la URL de la imagen del perfil del empleado
    profile_image_url = empleado.foto.url if empleado.foto else None

    return render(request, 'core/perfil_empleado.html', context={'empleado': empleado, 'form': form, 'profile_image_url': profile_image_url})





#Registrar un cliente
@login_required
@admin_required
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
@login_required
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
@login_required
@admin_required
def eliminar_empleado(request, empleado_id):
    empleado = Empleado.objects.get(pk=empleado_id)
    empleado.delete()
    return redirect('lista_empleados')


#Editar información de empleado
@login_required
@admin_required
def editar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, pk=empleado_id)
    if request.method == 'POST':
        form = EmpleadoEditarForm(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('lista_empleados')  # Asume que tienes una URL nombrada 'lista_empleados'
    else:
        form = EmpleadoEditarForm(instance=empleado)
    
    return render(request, 'core/editar_empleado.html', {'form': form})


#Editar información de cliente
@login_required
@admin_required
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
@login_required
@admin_required
def eliminar_cliente(request, cliente_id):
    cliente = Cliente.objects.get(pk=cliente_id)
    cliente.delete()
    return redirect('lista_clientes')


#perfil cliente 
@login_required
@admin_required
def perfil_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'core/perfil_cliente.html', {'cliente': cliente})

#Descargar archivos
@login_required
def descargar_archivos(request, archivo_id):
    archivo = get_object_or_404(Archivo, id=archivo_id)
    file_path = archivo.archivo.path
    return FileResponse(open(file_path, 'rb'))

#guardar archivos
@login_required
def guardar_archivos(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        files = request.FILES.getlist('files[]')

        try:
            cliente = Cliente.objects.get(pk=cliente_id)
        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

        for file in files:
            fs = FileSystemStorage()  # usar el sistema de almacenamiento de archivos de Django
            filename = fs.save(file.name, file)  # guardar el archivo
            file_url = fs.url(filename)  # obtener la URL del archivo

            # Crear y guardar la instancia del modelo Archivo
            Archivo.objects.create(cliente=cliente, archivo=filename)

        # Obtener todos los archivos para el cliente y devolverlos
        archivos_cliente = cliente.archivos.all()
        archivos_info = [{
            'name': archivo.archivo.name, 
            'url': archivo.archivo.url
        } for archivo in archivos_cliente]

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


#TICKET_FORM
@login_required
def crear_actualizar_ticket(request):
    if request.method == 'POST':
        # Lógica para manejar los datos del formulario
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            # Procesar el formulario aquí
            
            # Manejar archivo adjunto si está presente
            archivo_adjunto = request.FILES.get('archivo_adjunto')
            if archivo_adjunto:
                fs = FileSystemStorage()
                filename = fs.save(archivo_adjunto.name, archivo_adjunto)
                # Puedes almacenar el nombre del archivo en la base de datos si es necesario

            # Cambiar el nombre del archivo si se proporciona uno nuevo
            nuevo_nombre_archivo = request.POST.get('nuevo_nombre_archivo')
            if nuevo_nombre_archivo and archivo_adjunto:
                # Lógica para cambiar el nombre del archivo adjunto
                old_path = fs.path(filename)
                new_path = fs.path(nuevo_nombre_archivo)
                os.rename(old_path, new_path)

            # Redirigir a alguna página de éxito o renderizar otro template
            return redirect('pagina_exito')

    else:
        form = TicketForm()
    
    return render(request, 'ticket_form.html', {'form': form})


#TRELLO
@login_required
def crear_tabla(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        
        if form.is_valid():
            table = form.save()
            # Redirecciona al perfil del empleado después de guardar la tabla
            return redirect('table_list') 
    else:
        form = TableForm()
    
    tables = Table.objects.all()
    return render(request, 'core/table_list.html', {'form': form, 'tables': tables})

@login_required
def table_list(request):
    tables = Table.objects.all()
    tickets = Ticket.objects.all()  # Obtener todos los tickets
    
    return render(request, 'core/table_list.html', {'tables': tables, 'tickets': tickets})

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

            return redirect('table_list') 
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
            return redirect('table_list')  # Redirige a donde desees después de cargar el archivo
    else:
        form = TicketAttachmentForm()
    return render(request, 'upload_attachment.html', {'form': form})

#Actualizar ticket 
"""@login_required
def ticket_update(request, ticket_id):
    attachment_form = TicketAttachmentForm(request.POST, request.FILES)
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('table_list')
    else:
        # Aquí, asegúrate de pasar el ticket existente al formulario
        form = TicketForm(instance=ticket)
    return render(request, 'core/ticket_form.html', {'form': form})"""



@login_required
def ticket_update(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, instance=ticket)
        attachment_form = TicketAttachmentForm(request.POST, request.FILES)
        if ticket_form.is_valid() and attachment_form.is_valid():
            # Guardar el formulario del ticket actualizado
            ticket = ticket_form.save()

            # Guardar el formulario del archivo adjunto
            attachment = attachment_form.save(commit=False)
            attachment.ticket = ticket  # Asociar el archivo adjunto con el ticket
            attachment.save()
           

            return redirect('table_list')
    else:
        ticket_form = TicketForm(instance=ticket)  # Pasar la instancia del ticket al formulario
        attachments = TicketAttachment.objects.filter(ticket=ticket)
        attachment_form = TicketAttachmentForm()  # Formulario para nuevos archivos adjuntos

    return render(request, 'core/ticket_form.html', {'ticket_form': ticket_form, 'attachment_form': attachment_form, 'attachments': attachments})


@login_required
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket.delete()
    return redirect('table_list')

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


#*************************************************** PROYECTOS ********************************************************#
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

def lista_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'core/proyectos.html', {'proyectos': proyectos})

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
    tareas = Tareas.objects.all()
    return render(request, 'core/lista_tareas.html', {'tareas': tareas})


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
