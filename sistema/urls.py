from django.urls import path
from django.contrib.auth import views as auth_views
from sistema import views

app_name = 'sistema'

# URL configuration for the 'sistema' app
urlpatterns = [
    # --------------------------------------------
    # 1. Autenticación y Cuenta de Usuario
    # --------------------------------------------
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change_form'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    # --------------------------------------------
    # 2. Vistas Principales y Redirección
    # --------------------------------------------
    path('home/', views.HomeView.as_view(), name='home'),
    path('redireccion-por-rol/', views.redireccion_por_rol, name='redireccion_por_rol'),
    path('pendiente-aprobacion/', views.pendiente_aprobacion, name='pendiente_aprobacion'),
    path('analisis-dashboard/', views.analisis_dashboard, name='analisis_dashboard'),

    # --------------------------------------------
    # 3. Panel de Administración y Gestión de Usuarios
    # --------------------------------------------
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('usuarios/asignar_rol/<int:user_id>/', views.asignar_rol, name='asignar_rol'),
    path('registro/', views.registro, name='registro'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    # --------------------------------------------
    # 4. Paneles Específicos por Rol
    # --------------------------------------------
    #path('monitoreo-dashboard/', views.monitoreo_dashboard, name='monitoreo_dashboard'),
    
    #path('expedientes-dashboard/', views.expedientes_dashboard, name='expedientes_dashboard'),
    #path('relevamiento-dashboard/', views.relevamiento_dashboard, name='relevamiento_dashboard'),
    #path('sig-dashboard/', views.sig_dashboard, name='sig_dashboard'),

    # --------------------------------------------
    # 5. Otras URLs (comentadas para desarrollo)
    # --------------------------------------------
    #path('gerente-dashboard/', views.gerente_dashboard, name='gerente_dashboard'),         
   
]
