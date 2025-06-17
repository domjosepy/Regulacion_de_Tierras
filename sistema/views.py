from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
#from django.utils.decorators import method_decorator
#from django_ratelimit.decorators import ratelimit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import CreateView, TemplateView
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
# App local
from .forms import UserUpdateForm, CustomUserCreationForm, AsignarRolForm, UserCreationForm, CrearUsuarioForm
from .models import User, Notificacion

# ==============================================
# VISTA DE LOGIN PERSONALIZADA
# ==============================================
#@method_decorator(ratelimit(key='ip', rate='5/m'), name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos. 🔒")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, f"¡Bienvenido, {form.get_user().username}! 🎉")
        return super().form_valid(form)

    def get_success_url(self):
        # Elimina la redirección fija a 'home'
        redirect_to = self.request.POST.get('next', self.request.GET.get('next', ''))
        if redirect_to:
            return redirect_to
        return reverse_lazy('sistema:redireccion_por_rol')  # Redirige al sistema de roles

# ==============================================
# REDIRECCIÓN POR ROL
# ==============================================
@login_required
def redireccion_por_rol(request):
    if request.user.is_superuser or request.user.rol == 'ADMIN':
        return redirect('sistema:admin_dashboard')
    elif request.user.rol == 'GERENTE':
        return redirect('sistema:gerente_dashboard')
    elif request.user.rol == 'MONITOREO':
        return redirect('monitoreo_dashboard')
    elif request.user.rol == 'ANALISIS':
        return redirect('sistema:analisis_dashboard')
    elif request.user.rol == 'EXPEDIENTES':
        return redirect('sistema:expedientes_dashboard')
    elif request.user.rol == 'RELEVAMIENTO':
        return redirect('sistema:relevamiento_dashboard')
    elif request.user.rol == 'SIG':
        return redirect('sig_dashboard')
    else:
        # Usuarios pendientes o sin rol
        return redirect('pendiente_aprobacion')
# ==============================================
# VISTA DE PENDIENTE DE APROBACIÓN
# ==============================================
@login_required    
def pendiente_aprobacion(request):
    return render(request, 'pendiente_aprobacion.html')
    
# ==============================================
# VISTA DE HOME PROTEGIDA
# ==============================================
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

# ==============================================
# VISTA DE REGISTRO PERSONALIZADA
# ==============================================
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("sistema:login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        messages.success(self.request, "¡Registro exitoso! Por favor inicia sesión. ✅")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error en el registro. Revisa los datos. ❌")
        return super().form_invalid(form)
    
# =================================
# VISTA DE REGISTRO PERSONALIZADA 
# =================================
class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = 'PENDIENTE'
        if commit:
            user.save()
        return user

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)          
            Notificacion.crear_nuevo_usuario(user)
            return redirect('sistema:home')
    else:
        form = RegistroForm()
    
    return render(request, 'administrador/registro.html', {'form': form})

def is_admin(user):
    return user.is_superuser or user.rol == 'ADMIN'

@login_required
@user_passes_test(is_admin)
def crear_usuario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, f'Usuario {user.username} creado exitosamente')
                return redirect('sistema:gestion_usuarios')
            except Exception as e:
                messages.error(request, f'Error al crear usuario: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario')
    else:
        form = CrearUsuarioForm()
    
    return render(request, 'administrador/crear_usuario.html', {'form': form})

# ==============================================
# VISTA DE CAMBIO DE CONTRASEÑA PERSONALIZADA
# ==============================================
class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("sistema:home")

    def form_valid(self, form):
        messages.success(self.request, "Contraseña actualizada correctamente. 🔑")
        return super().form_valid(form)

# ==============================================
# VISTA DE LOGOUT PERSONALIZADA
# ==============================================
def custom_logout(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente. 👋")
    return redirect('sistema:login')

# ==============================================
# VISTA DE GESTIÓN DE USUARIOS
# ==============================================
@login_required
@permission_required('sistema.asignar_roles', raise_exception=True)
def asignar_rol(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        form = AsignarRolForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Rol actualizado correctamente para {usuario.username}')
            return redirect('sistema:gestion_usuarios')
    else:
        form = AsignarRolForm(instance=usuario)
    
    context = {
        'form': form,
        'usuario': usuario,
        'current_rol': usuario.get_rol_display(),
    }
    
    return render(request, 'administrador/asignar_rol.html', context)

# ==============================================
# VISTA DE DASHBOARD ADMINISTRATIVO
# ==============================================
def is_admin(user):
    return user.is_superuser or user.rol == 'ADMIN'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Obtener estadísticas
    total_usuarios = User.objects.count()
    usuarios_pendientes = User.objects.filter(rol='PENDIENTE')
    usuarios_activos = User.objects.filter(is_active=True).exclude(rol='PENDIENTE')
    nuevos_usuarios = User.objects.order_by('-date_joined')[:10]
    ultima_actividad = User.objects.latest('last_login').last_login if User.objects.exists() else timezone.now()
    
    context = {
        'total_usuarios': total_usuarios,
        'usuarios_pendientes': usuarios_pendientes,
        'usuarios_activos': usuarios_activos,
        'nuevos_usuarios': nuevos_usuarios,
        'ultima_actividad': ultima_actividad,
    }
    return render(request, 'administrador/admin_dashboard.html', context)

# ==============================================
# VISTA DE CREACIÓN DE USUARIO PARA ADMINISTRADOR
# ==============================================
@login_required
@user_passes_test(is_admin)
def crear_usuario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuario {user.username} creado exitosamente')
            return redirect('sistema:admin_dashboard')
    else:
        form = CrearUsuarioForm()
    
    return render(request, 'administrador/crear_usuario.html', {'form': form})
# ==============================================
# VISTA AJAX PARA ASIGNAR ROL Y ACTIVO
# ==============================================
def asignar_rol_ajax(request):
    """
    Vista AJAX para asignar rol y estado activo a un usuario.
    """
    if request.method == 'POST' and request.headers.get("x-requested-with") == "XMLHttpRequest":
        try:
            user_id = request.POST.get('user_id')
            rol = request.POST.get('rol')
            is_active = request.POST.get('is_active') == 'on'

            usuario = User.objects.get(pk=user_id)
            usuario.rol = rol
            usuario.is_active = is_active
            usuario.save()

            return JsonResponse({
                'success': True,
                'message': 'Rol actualizado correctamente'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    }, status=405)

                                                                    # VISTA DE DASHBOARD DE ANÁLISIS
                                                            # ============================================== 
@login_required
@user_passes_test(lambda u: u.rol == 'ANALISIS', login_url='sistema:pendiente_aprobacion')
def analisis_dashboard(request):
    # Aquí puedes agregar la lógica específica para el dashboard de análisis
    # Por ejemplo, estadísticas, gráficos, etc.
    return render(request, 'analisis/analisis_dashboard.html')
    


# ==============================================
# EDICIÓN DE PERFIL
# ==============================================
@login_required
def edit_profile(request):
    form = UserUpdateForm(request.POST or None, instance=request.user)

    if request.method == 'POST':
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
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {form.fields[field].label}: {error}")
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "success": False,
                    "message": "Errores en el formulario",
                    "errors": form.errors.get_json_data()
                })

    return render(request, "registration/edit_profile.html", {"form": form})

# ==============================================
# TESTEO DE TOASTS (SOLO PARA DESARROLLO)
# ==============================================
@login_required
def test_toast(request):
    messages.success(request, "¡Toast de prueba funciona correctamente! 🎉")
    messages.warning(request, "Este es un mensaje de advertencia. ⚠️")
    messages.error(request, "Este es un mensaje de error. ❌")
    messages.info(request, "Novedades disponibles 📢")
    return redirect("sistema:home")
