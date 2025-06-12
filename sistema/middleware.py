from django.shortcuts import redirect
from django.urls import reverse

class VerificacionRolMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if (request.user.is_authenticated and 
            not request.user.is_superuser and 
            hasattr(request.user, 'rol') and 
            request.user.rol == 'PENDIENTE' and
            not request.path.startswith('/static/') and
            request.path != reverse('sistema:pendiente_aprobacion') and
            request.path != reverse('sistema:logout')):
            return redirect('sistema:pendiente_aprobacion')
            
        return response