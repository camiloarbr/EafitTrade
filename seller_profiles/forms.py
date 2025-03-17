from django import forms
from .models import SellerProfile, Schedule
from django.forms import inlineformset_factory

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['profile_image', 'store_name', 'slogan', 'description']
        widgets = {
            'store_name': forms.TextInput(attrs={'class': 'form-control'}),
            'slogan': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

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
                'min': '07:00',
                'max': '22:00'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control time-input',
                'type': 'time',
                'min': '07:00',
                'max': '22:00'
            }),
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