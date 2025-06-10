from django import forms
from .models import Venta, VentaDetalle
from empleados.models import Empleado
from clientes.models import Cliente
from inventario.models import Bodega, Municipio
from zonas.models import Zona


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'vendedor','descuento', 'latitud', 'longitud',  'municipio', 'zona','total', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'vendedor': forms.Select(attrs={'class': 'form-select'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
            'municipio': forms.Select(attrs={'class': 'form-select'}),
            'zona': forms.Select(attrs={'class': 'form-select'}),
            'latitud': forms.NumberInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'step': 'any', 'id': 'id_latitud'}),
            'longitud': forms.NumberInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'step': 'any', 'id': 'id_longitud'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'total': forms.HiddenInput(),

        }

    def clean_descuento(self):
        descuento = self.cleaned_data.get('descuento')
        if descuento < 0 or descuento > 100:
            raise forms.ValidationError("El descuento debe estar entre 0% y 100%")
        return descuento

    def clean(self):
        cleaned_data = super().clean()
        lat = cleaned_data.get("latitud")
        lon = cleaned_data.get("longitud")

        if lat is None or lon is None:
            raise forms.ValidationError("La ubicación GPS es obligatoria")

        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise forms.ValidationError("Coordenadas inválidas")

        return cleaned_data


class VentaDetalleForm(forms.ModelForm):
    class Meta:
        model = VentaDetalle
        fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'step': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        }

class FiltroMapaVentasForm(forms.Form):
    fecha_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    vendedor = forms.ModelChoiceField(queryset=Empleado.objects.all(), required=False)

    municipio = forms.ChoiceField(required=False)
    zona = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar solo los municipios y zonas que están presentes en ventas
        municipios_ids = Venta.objects.values_list('municipio', flat=True).distinct()
        zonas_ids = Venta.objects.values_list('zona', flat=True).distinct()

        municipios = Municipio.objects.filter(id__in=municipios_ids).order_by('nombre')
        zonas = Zona.objects.filter(id__in=zonas_ids).order_by('nombre')

        self.fields['municipio'].choices = [('', 'Todos')] + [(m.id, str(m)) for m in municipios]
        self.fields['zona'].choices = [('', 'Todas')] + [(z.id, str(z)) for z in zonas]

        self.fields['municipio'].widget.attrs.update({'class': 'form-select select2'})
        self.fields['zona'].widget.attrs.update({'class': 'form-select select2'})
        self.fields['vendedor'].widget.attrs.update({'class': 'form-select select2'})



from django.forms import inlineformset_factory

VentaDetalleFormSet = inlineformset_factory(
    Venta, VentaDetalle,
    form=VentaDetalleForm,
    extra=1,
    can_delete=True
)
