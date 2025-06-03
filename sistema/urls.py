from django.urls import path
from django.contrib.auth import views as auth_views
from sistema import views

app_name = 'sistema'

# URL configuration for the 'sistema' app
urlpatterns = [
    # Inicio de Sesión, Crear Cuenta, Inicio, Password Change, Edit Profile, and Test Toast URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('password_change/', views.CustomPasswordChangeView.as_view(),
         name='password_change_form'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('logouth/', auth_views.LogoutView.as_view(), name='logout'),
    path('test_toast/', views.test_toast, name='test_toast'),

    # GESTION DE USUARIOS DESDE EL ADMIN
    path('usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('usuarios/asignar_rol/<int:user_id>/',
         views.asignar_rol, name='asignar_rol'),
]
