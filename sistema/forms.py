from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from .models import User


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