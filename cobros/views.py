from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import RutaCobro, Cuota, Pago
from .forms import RutaCobroForm, CuotaForm, PagoForm


# --- RutaCobro ---
class RutaCobroListView(ListView):
    model = RutaCobro
    template_name = 'bonanza_cobros/ruta_list.html'
    context_object_name = 'rutas'


class RutaCobroCreateView(CreateView):
    model = RutaCobro
    form_class = RutaCobroForm
    template_name = 'bonanza_cobros/ruta_form.html'
    success_url = reverse_lazy('bonanza_cobros:ruta_list')


class RutaCobroUpdateView(UpdateView):
    model = RutaCobro
    form_class = RutaCobroForm
    template_name = 'bonanza_cobros/ruta_form.html'
    success_url = reverse_lazy('bonanza_cobros:ruta_list')


class RutaCobroDeleteView(DeleteView):
    model = RutaCobro
    template_name = 'bonanza_cobros/ruta_confirm_delete.html'
    success_url = reverse_lazy('bonanza_cobros:ruta_list')


# --- Cuota ---
class CuotaListView(ListView):
    model = Cuota
    template_name = 'bonanza_cobros/cuota_list.html'
    context_object_name = 'cuotas'


class CuotaCreateView(CreateView):
    model = Cuota
    form_class = CuotaForm
    template_name = 'bonanza_cobros/cuota_form.html'
    success_url = reverse_lazy('bonanza_cobros:cuota_list')


class CuotaUpdateView(UpdateView):
    model = Cuota
    form_class = CuotaForm
    template_name = 'bonanza_cobros/cuota_form.html'
    success_url = reverse_lazy('bonanza_cobros:cuota_list')


class CuotaDeleteView(DeleteView):
    model = Cuota
    template_name = 'bonanza_cobros/cuota_confirm_delete.html'
    success_url = reverse_lazy('bonanza_cobros:cuota_list')


# --- Pago ---
class PagoListView(ListView):
    model = Pago
    template_name = 'bonanza_cobros/pago_list.html'
    context_object_name = 'pagos'


class PagoCreateView(CreateView):
    model = Pago
    form_class = PagoForm
    template_name = 'bonanza_cobros/pago_form.html'
    success_url = reverse_lazy('bonanza_cobros:pago_list')


class PagoUpdateView(UpdateView):
    model = Pago
    form_class = PagoForm
    template_name = 'bonanza_cobros/pago_form.html'
    success_url = reverse_lazy('bonanza_cobros:pago_list')


class PagoDeleteView(DeleteView):
    model = Pago
    template_name = 'bonanza_cobros/pago_confirm_delete.html'
    success_url = reverse_lazy('bonanza_cobros:pago_list')
