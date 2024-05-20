from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import crear_proyecto, lista_empleados, lista_proyectos, registro_cliente, registro_empleado
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    #***************************************La página de inicio será el TRELLO**************************************************
    path('', views.table_list, name='table_list'), 
    
#****************************** LOGIN ******************************#
    path('iniciar-sesion/', LoginView.as_view(template_name='core/login.html'), name='login'), #http://127.0.0.1:8000/iniciar-sesion/
    path('cerrar-sesion/', LogoutView.as_view(next_page='login'), name='logout'), #Tiene cerrar sesión y se le redirigirá al login

#****************************** EMPLEADOS ******************************#
    path('empleados/', lista_empleados, name='lista_empleados'), #http://127.0.0.1:8000/empleados/
    path('eliminar_empleado/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'), #para eliminar empleado
    path('perfil/<int:empleado_id>/', views.perfil_empleado, name='perfil_empleado'), #http://127.0.0.1:8000/perfil
    path('descargar-pdf/<int:empleado_id>/', views.descargar_pdf, name='descargar_pdf'), #para descargar pdf del empleado seleccionado
    path('editar_empleado/<int:empleado_id>/', views.editar_empleado, name='editar_empleado'), #http://127.0.0.1:8000/editar (por id de empleado)
    path('registrarme/', registro_empleado, name='registro_empleado'), #http://127.0.0.1:8000/registrarme/

#****************************** CLIENTE ******************************#
 
    path('clientes/', views.lista_clientes, name='lista_clientes'), #http://127.0.0.1:8000/lista_clientes
    path('registrar-cliente/', registro_cliente, name='registro_cliente'), #http://127.0.0.1:8000/registrar-cliente/
    path('editar_cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'), #http://127.0.0.1:8000/editar (por id de cliente)
    path('eliminar_cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'), #para eliminar cliente
    path('perfil_cliente/<int:cliente_id>/', views.perfil_cliente, name='perfil_cliente'),#Perfil clientes
    path('archivo/<int:archivo_id>/eliminar/', views.eliminar_archivo, name='eliminar_archivo'), #eliminar archivo
    path('guardar_archivos/', views.guardar_archivos, name='guardar_archivos'),#Guardar archivos clientes
    path('cambiar_nombre_archivo/<int:archivo_id>/', views.cambiar_nombre_archivo, name='cambiar_nombre_archivo'), #edición nombre archivo
    path('descargar_archivo/<int:archivo_id>/', views.descargar_archivos, name='descargar_archivos'),
   
#****************************** TRELLO ******************************#
    path('eliminar_tabla/<int:table_id>/', views.eliminar_tabla, name='eliminar_tabla'),#Eliminar tabla
    path('table_list/', views.table_list, name='table_list'),#Trello
    path('crear-tabla/', views.crear_tabla, name='crear_tabla'),#Crear tabla
    path('table/<int:table_id>/', views.table_detail, name='table_detail'),#Id de la tabla en especifico
    path('table/<int:table_id>/ticket/create/', views.ticket_create, name='ticket_create'),#Crear tickets
    path('ticket/<int:ticket_id>/update/', views.ticket_update, name='ticket_update'),#actualizar tickets
    path('ticket/<int:ticket_id>/delete/', views.ticket_delete, name='ticket_delete'),#eliminar tickets

#****************************** PROYECTOS Y TAREAS ******************************#
    path('proyectos/crear/', views.crear_proyecto, name='crear_proyecto'),
    path('proyectos/', lista_proyectos, name='lista_proyectos'),
    path('proyectos/<int:proyecto_id>/eliminar', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('proyectos/<int:proyecto_id>/editar/', views.editar_proyecto, name='editar_proyecto'),

    path('tareas/crear/', views.crear_tarea, name='crear_tarea'),
    path('tareas/', views.lista_tareas, name='lista_tareas'),
    path('tareas/<int:tarea_id>/editar', views.editar_tarea, name='editar_tarea'),
    path('tareas/<int:tarea_id>/eliminar', views.eliminar_tarea, name='eliminar_tarea'),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
