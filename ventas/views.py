from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from .models import Venta, VentaDetalle
from .forms import VentaForm, VentaDetalleFormSet, FiltroMapaVentasForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.forms import inlineformset_factory
from .models import Venta
from datetime import datetime
from django.db.models import Sum, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import TruncDate

class MapaVentasView(LoginRequiredMixin, TemplateView):
    template_name = 'bonanza_ventas/mapa_ventas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = FiltroMapaVentasForm(self.request.GET or None)
        ventas = Venta.objects.filter(latitud__isnull=False, longitud__isnull=False)

        if form.is_valid():
            fecha_inicio = form.cleaned_data.get('fecha_inicio')
            fecha_fin = form.cleaned_data.get('fecha_fin')
            vendedor = form.cleaned_data.get('vendedor')
            municipio = form.cleaned_data.get('municipio')
            zona = form.cleaned_data.get('zona')

            if fecha_inicio:
                ventas = ventas.filter(fecha__gte=fecha_inicio)
            if fecha_fin:
                ventas = ventas.filter(fecha__lte=fecha_fin)
            if vendedor:
                ventas = ventas.filter(vendedor=vendedor)
            if municipio:
                ventas = ventas.filter(municipio__icontains=municipio)
            if zona:
                ventas = ventas.filter(zona__icontains=zona)

        # Estadísticas
        total_ventas = ventas.count()
        suma_total = ventas.aggregate(total=Sum('total'))['total'] or 0

        # Ventas por vendedor
        ventas_por_vendedor = ventas.values('vendedor__nombres').annotate(total=Sum('total')).order_by('-total')

        # Ventas por fecha
        ventas_por_fecha = ventas.annotate(fecha_dia=TruncDate('fecha')) \
                                 .values('fecha_dia') \
                                 .annotate(total=Sum('total')) \
                                 .order_by('fecha_dia')

        context.update({
            'form': form,
            'ventas': ventas,
            'total_ventas': total_ventas,
            'suma_total': suma_total,
            'ventas_por_vendedor': list(ventas_por_vendedor),
            'ventas_por_fecha': list(ventas_por_fecha),
        })
        return context



class VentaListView(ListView):
    model = Venta
    template_name = 'bonanza_ventas/venta_list.html'
    context_object_name = 'ventas'
    paginate_by = 10

class VentaCreateView(LoginRequiredMixin, CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'bonanza_ventas/venta_form.html'
    success_url = reverse_lazy('ventas:venta_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['detalle_formset'] = VentaDetalleFormSet(self.request.POST)
        else:
            context['detalle_formset'] = VentaDetalleFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        detalle_formset = context['detalle_formset']
        if detalle_formset.is_valid():
            form.instance.usuario_creador = self.request.user
            self.object = form.save(commit=False)

            total = 0
            for detalle in detalle_formset:
                producto = detalle.cleaned_data.get('producto')
                cantidad = detalle.cleaned_data.get('cantidad')
                if producto and cantidad:
                    total += producto.precio * cantidad

            descuento = form.cleaned_data.get('descuento') or 0
            self.object.total = total * (1 - descuento / 100)
            self.object.save()

            detalle_formset.instance = self.object
            detalle_formset.save()

            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class VentaUpdateView(UpdateView):
    model = Venta
    form_class = VentaForm
    template_name = 'bonanza_ventas/venta_form.html'
    success_url = reverse_lazy('bonanza_ventas:venta_list')

class VentaDeleteView(DeleteView):
    model = Venta
    template_name = 'bonanza_ventas/venta_confirm_delete.html'
    success_url = reverse_lazy('bonanza_ventas:venta_list')

class VentaDetailView(DetailView):
    model = Venta
    template_name = 'bonanza_ventas/venta_detail.html'
    context_object_name = 'venta'

class VentaCreateUpdateView(View):
    template_name = 'bonanza_ventas/venta_form.html'
    success_url = reverse_lazy('bonanza_ventas:venta_list')

    def get(self, request, pk=None):
        venta = None
        if pk:
            venta = get_object_or_404(Venta, pk=pk)
        form = VentaForm(instance=venta)

        VentaDetalleFormSet = inlineformset_factory(
            Venta, VentaDetalle,
            form=VentaDetalleForm,
            extra=1,
            can_delete=True
        )

        formset = VentaDetalleFormSet(instance=venta)
        return render(request, self.template_name, {'form': form, 'detalles': formset, 'object': venta})

    def post(self, request, pk=None):
        venta = None
        if pk:
            venta = get_object_or_404(Venta, pk=pk)
        form = VentaForm(request.POST, instance=venta)

        VentaDetalleFormSet = inlineformset_factory(
            Venta, VentaDetalle,
            form=VentaDetalleForm,
            extra=1,
            can_delete=True
        )

        formset = VentaDetalleFormSet(request.POST, instance=venta)

        if form.is_valid() and formset.is_valid():
            venta_guardada = form.save()
            formset.instance = venta_guardada
            formset.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form, 'detalles': formset, 'object': venta})
