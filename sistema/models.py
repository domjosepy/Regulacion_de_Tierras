from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

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
    
    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"

    class Meta:
        permissions = [
            ("asignar_roles", "Puede asignar roles a usuarios"),
        ]