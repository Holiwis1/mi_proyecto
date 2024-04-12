from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import lista_empleados, registro_cliente, registro_empleado
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('empleados/', lista_empleados, name='lista_empleados'), #http://127.0.0.1:8000/empleados/
    path('registrarme/', registro_empleado, name='registro_empleado'), #http://127.0.0.1:8000/registrarme/
    path('iniciar-sesion/', LoginView.as_view(template_name='core/login.html'), name='login'), #http://127.0.0.1:8000/iniciar-sesion/
    path('clientes/', views.lista_clientes, name='lista_clientes'), #http://127.0.0.1:8000/lista_clientes
    path('perfil/<int:empleado_id>/', views.perfil_empleado, name='perfil_empleado'), #http://127.0.0.1:8000/perfil
    path('registrarme2/', registro_cliente, name='registro_cliente'), #http://127.0.0.1:8000/registrarme2/
    path('descargar-pdf/<int:empleado_id>/', views.descargar_pdf, name='descargar_pdf'),
    path('editar_empleado/<int:empleado_id>/', views.editar_empleado, name='editar_empleado'), #http://127.0.0.1:8000/editar (por id de empleado)
    path('eliminar_empleado/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'), #para eliminar empleado
    path('editar_cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'), #http://127.0.0.1:8000/editar (por id de cliente)
    path('eliminar_cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'), #para eliminar cliente
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
