from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from django.shortcuts import redirect, render
from django import forms

from django.http import JsonResponse
from .forms import UserUpdateForm


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        # Si el formulario es incorrecto, muestra un mensaje de error
        messages.error(self.request, "Usuario o contraseña incorrectos.")
        return super().form_invalid(form)

# esto funciona sin el from_invalid, from_valid
    def get_success_url(self):
        # Fuerza la redirección a home después de login
        return reverse_lazy('home')


class HomeView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/password_change_form.html"
    # Redirige a home después de cambiar la contraseña
    success_url = reverse_lazy("home")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro exitoso 🎉 ¡Bienvenido!")
            return redirect("home")
        else:
            messages.error(
                request, "Error en el formulario. Revisa los datos.")
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
            messages.success(request, "Perfil actualizado correctamente 🎉")
            return redirect('edit_profile')
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "success": False,
                    "message": "Error al guardar los datos. Revisa el formulario."
                })
            messages.error(request, "Hubo un error al actualizar los datos.")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "registration/edit_profile.html", {"form": form})


@login_required
def test_toast(request):
    messages.success(request, "🎉 Funciona el toast de Bootstrap 5 con Django.")
    return redirect("home")
