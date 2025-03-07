from django import forms
from .models import Product, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'description', 'quantity', 'price',
            'condition', 'location', 'image', 'payment_method',
            'account_number', 'account_type', 'qr_code', 'tags'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe tu producto detalladamente'
            }),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: Biblioteca, Bloque 18'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'account_type': forms.Select(attrs={'class': 'form-control'}),
            'qr_code': forms.FileInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: libro, matemáticas, cálculo'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].required = False
        self.fields['tags'].required = False
        
        # Campos de transferencia inicialmente no requeridos
        self.fields['account_number'].required = False
        self.fields['account_type'].required = False
        self.fields['qr_code'].required = False

        # Mejora de las etiquetas y mensajes de ayuda
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].label = f"{self.fields[field].label} *"

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        
        if payment_method == 'Transferencia':
            required_fields = {
                'account_number': 'número de cuenta',
                'account_type': 'tipo de cuenta',
                'qr_code': 'código QR'
            }
            
            for field, name in required_fields.items():
                if not cleaned_data.get(field):
                    self.add_error(field, f'El {name} es requerido para pagos por transferencia')
        
        return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Escribe tu comentario aquí...',
                'class': 'comment-input'
            }),
            'rating': forms.HiddenInput(attrs={
                'class': 'rating-input'
            })
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text.strip():
            raise forms.ValidationError('El comentario no puede estar vacío')
        if len(text) > 500:
            raise forms.ValidationError('El comentario no puede tener más de 500 caracteres')
        return text

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is None:
            raise forms.ValidationError('Debes asignar una calificación')
        if not (0 <= rating <= 5):
            raise forms.ValidationError('La calificación debe estar entre 0 y 5')
        return rating

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.'
        self.fields['password1'].help_text = '''
            <ul>
                <li>Tu contraseña no puede ser muy similar a tu otra información personal.</li>
                <li>Tu contraseña debe contener al menos 8 caracteres.</li>
                <li>Tu contraseña no puede ser una contraseña comúnmente utilizada.</li>
                <li>Tu contraseña no puede ser completamente numérica.</li>
            </ul>
        '''
        self.fields['password2'].help_text = 'Ingresa la misma contraseña que antes, para verificación.' 