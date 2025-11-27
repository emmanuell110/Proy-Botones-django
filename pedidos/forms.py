from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre_cliente', 'telefono', 'tipo_tamal', 'cantidad', 'comentarios']
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del cliente'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp'}),
            'tipo_tamal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rojo, verde, dulce, etc.'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Sin salsa, extra picante, hora de entrega, etc.'}),
        }
