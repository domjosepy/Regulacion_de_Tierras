from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import UserUpdateForm, CustomUserCreationForm, AsignarRolForm 
from .models import User

# Create your views here.

# VISTA LOGIN
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos. 🔒")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(
            self.request, f"¡Bienvenido, {form.get_user().username}! 🎉")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('sistema:home')

# VISTA DEL HOME
class HomeView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(
                request, "Debes iniciar sesión para acceder a esta página. 🔐")
            return redirect('sistema:login')
        return super().dispatch(request, *args, **kwargs)

# VISTA DE CREACION DE CUENTA
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("sistema:login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        messages.success(
            self.request, "¡Registro exitoso! Por favor inicia sesión. ✅")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Error en el registro. Revisa los datos. ❌")
        return super().form_invalid(form)

# CAMBIO DE CONTRASEÑA
class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("sistema:home")

    def form_valid(self, form):
        messages.success(
            self.request, "Contraseña actualizada correctamente. 🔑")
        return super().form_valid(form)

# VISTA DE LOGOUT
def custom_logout(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente. 👋")
    return redirect('sistema:login')



# ASIGNACION DE ROLES    
@login_required
@permission_required('sistema.asignar_roles', raise_exception=True)
def gestion_usuarios(request):
    # Usuarios con rol asignado
    usuarios_activos = User.objects.exclude(rol='PENDIENTE').order_by('-date_joined')
    
    # Usuarios pendientes
    usuarios_pendientes = User.objects.filter(rol='PENDIENTE').order_by('-date_joined')
    
    return render(request, 'sistema/gestion_usuarios.html', {
        'usuarios_activos': usuarios_activos,
        'usuarios_pendientes': usuarios_pendientes,
    })

@login_required
@permission_required('sistema.asignar_roles', raise_exception=True)
def asignar_rol(request, user_id):
    usuario = User.objects.get(pk=user_id)
    
    if request.method == 'POST':
        form = AsignarRolForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Rol asignado correctamente a {usuario.username}')
            return redirect('gestion_usuarios')
    else:
        form = AsignarRolForm(instance=usuario)
    
    return render(request, 'sistema/asignar_rol.html', {
        'form': form,
        'usuario': usuario,
    })

# CAMBIO DE DATOS PERSONALES
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "success": True,
                    "message": "Perfil actualizado correctamente 🎉",
                    "redirect_url": reverse("sistema:home")
                })
            messages.success(request, "Perfil actualizado correctamente. ✅")
            return redirect('edit_profile')
        else:
            # Agregar mensajes de error específicos
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {form.fields[field].label}: {error}")
            
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "success": False,
                    "message": "Errores en el formulario",
                    "errors": form.errors.get_json_data()
                })
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, "registration/edit_profile.html", {"form": form})


@login_required
def test_toast(request):
    messages.success(request, "¡Toast de prueba funciona correctamente!🎉")
    messages.warning(request, "Este es un mensaje de advertencia. ⚠️")
    messages.error(request, "Este es un mensaje de error. ❌")
    messages.info(request, "Novedades disponibles 📢")
    return redirect("sistema:home")
