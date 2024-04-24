from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import lista_empleados, registro_cliente, registro_empleado
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    #urls empleados
    path('empleados/', lista_empleados, name='lista_empleados'), #http://127.0.0.1:8000/empleados/
    path('eliminar_empleado/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'), #para eliminar empleado
    path('perfil/<int:empleado_id>/', views.perfil_empleado, name='perfil_empleado'), #http://127.0.0.1:8000/perfil
    path('descargar-pdf/<int:empleado_id>/', views.descargar_pdf, name='descargar_pdf'), #para descargar pdf del empleado seleccionado
    path('editar_empleado/<int:empleado_id>/', views.editar_empleado, name='editar_empleado'), #http://127.0.0.1:8000/editar (por id de empleado)
    path('registrarme/', registro_empleado, name='registro_empleado'), #http://127.0.0.1:8000/registrarme/
     #urls clientes
    path('iniciar-sesion/', LoginView.as_view(template_name='core/login.html'), name='login'), #http://127.0.0.1:8000/iniciar-sesion/
    path('clientes/', views.lista_clientes, name='lista_clientes'), #http://127.0.0.1:8000/lista_clientes
    path('registrarme2/', registro_cliente, name='registro_cliente'), #http://127.0.0.1:8000/registrarme2/
    path('editar_cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'), #http://127.0.0.1:8000/editar (por id de cliente)
    path('eliminar_cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'), #para eliminar cliente
    
   
    path('perfil_cliente/<int:cliente_id>/', views.perfil_cliente, name='perfil_cliente'),
    path('guardar_archivos/', views.guardar_archivos, name='guardar_archivos'), #para subir los archivos al la pagina web
    path('archivo/<int:archivo_id>/descargar/', views.descargar_archivos, name='descargar_archivos'), #para descargar los archivos

    #urls de trello
<<<<<<< Updated upstream
    path('eliminar_tabla/<int:table_id>/', views.eliminar_tabla, name='eliminar_tabla'),
    path('table_list/', views.table_list, name='table_list'),
    path('crear-tabla/', views.crear_tabla, name='crear_tabla'),
    path('table/<int:table_id>/', views.table_detail, name='table_detail'),
    path('table/<int:table_id>/ticket/create/', views.ticket_create, name='ticket_create'),
    path('ticket/<int:ticket_id>/update/', views.ticket_update, name='ticket_update'),
    path('ticket/<int:ticket_id>/delete/', views.ticket_delete, name='ticket_delete'),
    
=======
    path('eliminar_tabla/<int:table_id>/', views.eliminar_tabla, name='eliminar_tabla'),#Eliminar tabla
    path('table_list/', views.table_list, name='table_list'),#Trello
    path('crear-tabla/', views.crear_tabla, name='crear_tabla'),#Crear tabla
    path('table/<int:table_id>/', views.table_detail, name='table_detail'),#Id de la tabla en especifico
    path('table/<int:table_id>/ticket/create/', views.ticket_create, name='ticket_create'),#Crear tickets
    path('ticket/<int:ticket_id>/update/', views.ticket_update, name='ticket_update'),#Actualizar tickets
    path('ticket/<int:ticket_id>/delete/', views.ticket_delete, name='ticket_delete'),#Eliminar tickets
>>>>>>> Stashed changes
    

    #Guardar archivos clientes
    path('archivo/<int:archivo_id>/eliminar/', views.eliminar_archivo, name='eliminar_archivo'), #eliminar archivo
    path('guardar_archivos/', views.guardar_archivos, name='guardar_archivos'),#Guardar archivos clientes
    path('cambiar_nombre_archivo/<int:archivo_id>/', views.cambiar_nombre_archivo, name='cambiar_nombre_archivo'), #edición nombre archivo
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
