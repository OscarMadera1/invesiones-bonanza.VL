from django import forms
from .models import Zona

class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = ['nombre', 'municipio', 'descripcion', 'cobrador_asignado']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'municipio': forms.Select(attrs={'class':'form-control'})
        }
