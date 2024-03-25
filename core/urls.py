from django.urls import path
from .views import lista_empleados, registro_empleado
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('empleados/', lista_empleados, name='lista_empleados'), #http://127.0.0.1:8000/empleados/
    path('registrarme/', registro_empleado, name='registro_empleado'), #http://127.0.0.1:8000/registrarme/
    path('iniciar-sesion/', LoginView.as_view(template_name='core/login.html'), name='login'), #http://127.0.0.1:8000/iniciar-sesion/
]