from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from django.shortcuts import redirect, render
from django.http import JsonResponse
from .forms import UserUpdateForm


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
        return reverse_lazy('home')


class HomeView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(
                request, "Debes iniciar sesión para acceder a esta página. 🔐")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        messages.success(
            self.request, "¡Registro exitoso! Por favor inicia sesión. ✅")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Error en el registro. Revisa los datos. ❌")
        return super().form_invalid(form)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(
            self.request, "Contraseña actualizada correctamente. 🔑")
        return super().form_valid(form)


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Registro y autenticación exitosos! 🎉")
            return redirect("home")
        else:
            messages.error(
                request, "Error en el formulario. Revisa los datos. ❌")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


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
                    "redirect_url": reverse("home")
                })
            messages.success(request, "Perfil actualizado correctamente. ✅")
            return redirect('edit_profile')
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "success": False,
                    "message": "Error al guardar los datos. Revisa el formulario. ❌"
                })
            messages.error(request, "Error al actualizar el perfil. ❌")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, "registration/edit_profile.html", {"form": form})


@login_required
def test_toast(request):
    messages.success(request, "🎉 ¡Toast de prueba funciona correctamente!")
    messages.warning(request, "⚠️ Este es un mensaje de advertencia.")
    messages.error(request, "❌ Este es un mensaje de error.")
    messages.info(request, "📢 Novedades disponibles")
    return redirect("home")
