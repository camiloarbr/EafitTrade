from django import forms
from .models import SellerProfile, Schedule
from django.forms import inlineformset_factory
import re

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['profile_image', 'store_name', 'slogan', 'description', 'whatsapp']
        widgets = {
            'store_name': forms.TextInput(attrs={'class': 'form-control'}),
            'slogan': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '573001234567'
            }),
        }
        help_texts = {
            'store_name': 'Nombre visible de tu negocio para los compradores.',
            'slogan': 'Una frase corta que describa tu negocio (opcional).',
            'description': 'Describe tu negocio, qué productos vendes y cualquier información relevante para tus clientes.',
            'profile_image': 'Sube una imagen de tu logo o perfil (opcional).',
            'whatsapp': 'Número de WhatsApp para contacto (opcional). Formato: 573001234567.'
        }
        error_messages = {
            'store_name': {
                'required': 'Por favor ingresa un nombre para tu tienda.',
                'max_length': 'El nombre de la tienda no puede exceder los 100 caracteres.'
            },
            'description': {
                'required': 'Por favor ingresa una descripción para tu tienda.'
            }
        }

    def clean_whatsapp(self):
        whatsapp = self.cleaned_data.get('whatsapp')
        if whatsapp:
            # Eliminar cualquier espacio o carácter especial
            whatsapp = re.sub(r'[^0-9]', '', whatsapp)
            
            # Verificar que el número tenga el formato correcto
            if not re.match(r'^57[3]\d{9}$', whatsapp):
                raise forms.ValidationError(
                    'El número debe comenzar con 57 seguido de un 3 y 9 dígitos más. Ejemplo: 573001234567'
                )
            
            return whatsapp
        return None

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['day', 'is_available', 'start_time', 'end_time']
        widgets = {
            'day': forms.HiddenInput(),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input availability-toggle',
                'role': 'switch'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control time-input',
                'type': 'time',
                'min': '06:00',
                'max': '22:00'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control time-input',
                'type': 'time',
                'min': '06:00',
                'max': '22:00'
            }),
        }
        help_texts = {
            'is_available': 'Indica si estás disponible este día.',
            'start_time': 'Hora de inicio (entre 6:00 a.m. y 10:00 p.m.)',
            'end_time': 'Hora de cierre (entre 6:00 a.m. y 10:00 p.m.)'
        }

class ScheduleFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Si es un nuevo perfil
            self.initial = [
                {'day': day[0]} for day in Schedule.DAYS_OF_WEEK
            ]

ScheduleInlineFormSet = inlineformset_factory(
    SellerProfile,
    Schedule,
    formset=ScheduleFormSet,
    form=ScheduleForm,
    extra=0,
    min_num=5,
    max_num=5,
    validate_min=True,
    validate_max=True,
    can_delete=False
) 