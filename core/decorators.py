from django.http import HttpResponse
from functools import wraps
from django.shortcuts import redirect, render

#Decorador para autentificar que el usuario es el administrador
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Comprueba si el usuario está autenticado
        if not request.user.is_authenticated:
            # Redirige a la página de inicio de sesión
            return redirect('login') 

        # Comprueba si el usuario es administrador
        if request.user.rol != 'admin':
            # Renderiza una página de error específica para problemas de rol
            context = {'mensaje': 'No tienes permiso para ver esta página'}
            return render(request, 'core/rol_error.html', context, status=403)

        return view_func(request, *args, **kwargs)
    return _wrapped_view
