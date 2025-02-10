from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'description', 'quantity', 'price',
            'condition', 'location', 'image', 'payment_method',
            'account_number', 'account_type', 'qr_code', 'tags'
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe tu producto detalladamente'
            }),
            'tags': forms.TextInput(attrs={
                'placeholder': 'Ejemplo: libro, matemáticas, cálculo'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Ejemplo: Biblioteca, Bloque 18'
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