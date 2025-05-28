from django import forms
from .models import Cuota, Pago, RutaCobro
from django.core.exceptions import ValidationError
from django.utils import timezone


class RutaCobroForm(forms.ModelForm):
    class Meta:
        model = RutaCobro
        fields = ['nombre', 'municipio', 'zona', 'cobrador', 'fecha_programada']
        widgets = {
            'fecha_programada': forms.DateInput(attrs={'type': 'date'}),
        }


class CuotaForm(forms.ModelForm):
    class Meta:
        model = Cuota
        fields = ['cliente', 'monto', 'fecha_vencimiento']

    def clean_monto(self):
        monto = self.cleaned_data['monto']
        if monto <= 0:
            raise ValidationError("El monto debe ser mayor que cero.")
        return monto

    def clean_fecha_vencimiento(self):
        fecha = self.cleaned_data['fecha_vencimiento']
        if fecha < timezone.now().date():
            raise ValidationError("La fecha de vencimiento no puede ser en el pasado.")
        return fecha


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['cuota', 'cobrador', 'monto_pagado', 'fecha_pago', 'observaciones']
        widgets = {
            'fecha_pago': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        cuota = cleaned_data.get('cuota')
        monto_pagado = cleaned_data.get('monto_pagado')

        if cuota and cuota.pagado:
            raise ValidationError("Esta cuota ya ha sido pagada.")
