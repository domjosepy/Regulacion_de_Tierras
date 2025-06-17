from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# =================================================
# MODELO DE USUARIO PERSONALIZADO
# =================================================
class User(AbstractUser):
    # Heredamos de AbstractUser para extender el modelo User estándar
    ROLES = (
        ('PENDIENTE', 'Pendiente de asignación'),
        ('ADMIN', 'Administrador'),
        ('GERENTE', 'Gerente'),
        ('MONITOREO', 'Jefe de Monitoreo'),
        ('ANALISIS', 'Jefe de Análisis'),
        ('EXPEDIENTES', 'Jefe de Expedientes'),
        ('RELEVAMIENTO', 'Jefe de Relevamiento'),
        ('SIG', 'Jefe de SIG'),
    )
    ci = models.CharField(max_length=8, blank=True, null=True,
            validators=[RegexValidator(
                regex='^[0-9]{7,8}$',
                message='La cédula debe tener 7 u 8 dígitos, sin guiones, ni puntos.',
                code='invalid_ci'
            )],
            verbose_name = 'Cédula de Identidad'
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='PENDIENTE', verbose_name='Rol')
    telefono = models.CharField(max_length=10, blank=True, null=True, 
            validators=[RegexValidator(
                regex='^[0-9]{10}$',
                message='El teléfono debe tener 10 dígitos.',
                code='invalid_phone'
            )])
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def get_rol_display(self):
        return dict(self.ROLES).get(self.rol, self.rol)

    def get_rol_color(self):
        colors = {
            'ADMIN': 'primary',
            'GERENTE': 'info',
            'MONITOREO': 'info',
            'ANALISIS': 'info',
            'EXPEDIENTES': 'info',
            'RELEVAMIENTO': 'info',
            'SIG': 'info',
            'PENDIENTE': 'light',
        }
        return colors.get(self.rol, 'secondary')

    class Meta:
        permissions = [
            ("asignar_roles", "Puede asignar roles a usuarios"),
        ]

#=================================================
# MODELO DE NOTIFICACIONES
#=================================================
class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def crear_nuevo_usuario(cls, usuario_nuevo):
        admins = User.objects.filter(is_superuser=True)
        mensaje = f"Nuevo usuario registrado: {usuario_nuevo.username} ({usuario_nuevo.date_joined.strftime('%d/%m/%Y %H:%M')})"
        
        for admin in admins:
            Notificacion.objects.create(usuario=admin, mensaje=mensaje)