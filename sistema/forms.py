from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from .models import User

# ==============================================
# FORMULARIOS DE USUARIO
# ==============================================
class UserUpdateForm(forms.ModelForm):
    ci = forms.CharField(
        required=False,
        max_length=8,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: 12345678',
            'inputmode': 'numeric',
            'maxlength': '8',
            'class': 'form-control',
            'pattern': '[0-9]{6,7}'
        }),
        validators=[RegexValidator(
            regex='^[0-9]{7,8}$',
            message=_('La cédula debe tener entre 6 y 7 dígitos numéricos'),
            code='invalid_ci'
        )],
        help_text=_('Ingrese su cédula sin puntos ni guiones')
    )
    
    telefono = forms.CharField(
        required=False,
        max_length=10,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: 0999999999',
            'inputmode': 'numeric',
            'maxlength': '10',
            'class': 'form-control',
            'pattern': '[0-9]{10}'
        }),
        validators=[RegexValidator(
            regex='^[0-9]{10}$',
            message=_('El teléfono debe tener exactamente 10 dígitos'),
            code='invalid_phone'
        )],
        help_text=_('Ingrese su teléfono sin espacios ni guiones')
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'ci', 'telefono']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}), 
        }

# ==============================================
# FORMULARIOS DE REGISTRO PERSONALIZADO (signup)
# ==============================================
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 
                 'first_name', 'last_name', 'ci', 'telefono')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'ci': forms.TextInput(attrs={
                'placeholder': 'Ej: 12345678',
                'pattern': '[0-9]{6,7}',
                'title': '6 o 7 dígitos sin guiones',
                'inputmode': 'numeric',
                'maxlength': '7',
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '');"
            }),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Ej: 0999999999',
                'pattern': '[0-9]{10}',
                'title': '10 dígitos, sin guiones ni espacios',
                'inputmode': 'numeric',
                'maxlength': '10',
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '');"
            })
        }
        
        help_texts = {
            'username': 'Puede contener letras, números y @/./+/-/_',
            'ci': 'Cédula de identidad sin puntos ni guiones'
        }
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['ci'].required = False
        self.fields['telefono'].required = False
        self.fields['email'].required = False

#======================================================
# FORMULARIO DE CREACIÓN DE USUARIO PARA ADMINISTRADOR
#======================================================
class CrearUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'rol')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configuración de campos de contraseña
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
        # Configuración del campo rol
        self.fields['rol'] = forms.ChoiceField(
            choices=[(role, label) for role, label in User.ROLES if role != 'PENDIENTE'],
            initial='GERENTE',
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        # Mensajes de ayuda más claros
        self.fields['password1'].help_text = """
        <ul class="text-muted small">
            <li>Mínimo 8 caracteres</li>
            <li>No puede ser similar a otros datos personales</li>
            <li>No puede ser una contraseña común</li>
            <li>No puede ser completamente numérica</li>
        </ul>
        """

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Las contraseñas no coinciden")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Aseguramos que la contraseña se establezca correctamente
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
#======================================================
# FORMULARIO PARA ASIGNAR ROLES A USUARIOS EXISTENTES
#======================================================
class AsignarRolForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['rol', 'is_active']
        labels = {
            'is_active': 'Activar usuario',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtramos los roles que no son "PENDIENTE"
        self.fields['rol'].choices = [choice for choice in User.ROLES if choice[0] != 'PENDIENTE']