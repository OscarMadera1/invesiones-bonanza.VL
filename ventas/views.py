from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from .models import Venta, VentaDetalle
from .forms import FiltroMapaVentasForm, VentaForm, VentaDetalleForm
from datetime import datetime
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.forms import formset_factory
from inventario.models import Producto,Municipio
from zonas.models import Zona
import sweetify
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.db import transaction
from django.contrib import messages
from inventario.models import InventarioBodega
from django.http import JsonResponse

VentaDetalleFormSet = formset_factory(VentaDetalleForm, extra=1)

def stock_disponible(request):
    producto_id = request.GET.get('producto_id')
    bodega_id = request.GET.get('bodega_id')

    if not producto_id or not bodega_id:
        return JsonResponse({'success': False, 'error': 'Datos incompletos'})

    try:
        inventario = InventarioBodega.objects.get(producto_id=producto_id, bodega_id=bodega_id)
        return JsonResponse({'success': True, 'stock': inventario.cantidad})
    except InventarioBodega.DoesNotExist:
        return JsonResponse({'success': True, 'stock': 0})


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
                try:
                    municipio_obj = Municipio.objects.get(id=municipio)
                    ventas = ventas.filter(municipio=municipio_obj)
                except Municipio.DoesNotExist:
                    pass

            if zona:
                try:
                    zona_obj = Zona.objects.get(id=zona)
                    ventas = ventas.filter(zona=zona_obj)
                except Zona.DoesNotExist:
                    pass

        # Estadísticas
        total_ventas = ventas.count()
        suma_total = ventas.aggregate(total=Sum('total'))['total'] or 0

        # Agrupación para gráficos
        ventas_por_vendedor = ventas.values('vendedor__nombre') \
            .annotate(total=Sum('total')) \
            .order_by('-total')

        ventas_por_fecha = ventas.annotate(fecha_dia=TruncDate('fecha_venta')) \
            .values('fecha_dia') \
            .annotate(total=Sum('total')) \
            .order_by('fecha_dia')

        # Serializar datos relevantes para el mapa
        ventas_serializadas = [
            {
                'id': v.id,
                'latitud': v.latitud,
                'longitud': v.longitud,
                'cliente': v.cliente.nombre,
                'vendedor': v.vendedor.nombre,
                'total': float(v.total),
            }
            for v in ventas
            if v.latitud and v.longitud
        ]

        # Totales y estadísticas
        total_ventas = ventas.count()
        suma_total = ventas.aggregate(Sum('total'))['total__sum'] or 0

        # Gráficos
        ventas_por_vendedor = ventas.values('vendedor__nombre').annotate(total=Sum('total'))
        labels_vendedor = [v['vendedor__nombre'] for v in ventas_por_vendedor]
        data_vendedor = [float(v['total']) for v in ventas_por_vendedor]

        ventas_por_fecha = ventas.values('fecha_venta').annotate(total=Sum('total')).order_by('fecha_venta')
        labels_fecha = [v['fecha_venta'].strftime('%Y-%m-%d') for v in ventas_por_fecha]
        data_fecha = [float(v['total']) for v in ventas_por_fecha]

        context.update({
            'form': form,
            'ventas': ventas,
            'total_ventas': total_ventas,
            'suma_total': suma_total,
            'ventas_por_vendedor': list(ventas_por_vendedor),
            'ventas_por_fecha': list(ventas_por_fecha),
            'labels_vendedor': json.dumps(labels_vendedor, cls=DjangoJSONEncoder),
            'data_vendedor': json.dumps(data_vendedor, cls=DjangoJSONEncoder),
            'labels_fecha': json.dumps(labels_fecha, cls=DjangoJSONEncoder),
            'data_fecha': json.dumps(data_fecha, cls=DjangoJSONEncoder),
            'ventas_json': json.dumps(ventas_serializadas, cls=DjangoJSONEncoder),

        })
        return context


class VentaListView(ListView):
    model = Venta
    template_name = 'bonanza_ventas/venta_list.html'
    context_object_name = 'ventas'
    paginate_by = 10



class VentaCreateView(LoginRequiredMixin, View):
    template_name = 'bonanza_ventas/venta_form.html'
    success_url = reverse_lazy('ventas:venta_list')

    def get(self, request, *args, **kwargs):
        form = VentaForm()
        productos = Producto.objects.all()
        return render(request, self.template_name, {
            'form': form,
            'productos': productos
        })

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = VentaForm(request.POST)
        productos = Producto.objects.all()
        detalles = self._obtener_detalles_desde_post(request.POST)

        if form.is_valid() and detalles:
            zona = form.cleaned_data['zona']

            # ⚠️ Asegúrate de tener zona.bodega o ajusta esto según tu modelo
            try:
                bodega = zona.bodega
            except AttributeError:
                sweetify.error(request, title="Error", text="La zona seleccionada no tiene una bodega asignada.")
                return render(request, self.template_name, {'form': form, 'productos': productos})

            errores_stock = []

            for d in detalles:
                producto = d['producto']
                cantidad = d['cantidad']

                inventario = InventarioBodega.objects.filter(bodega=bodega, producto=producto).first()

                if not inventario:
                    errores_stock.append(f"El producto '{producto.nombre}' no está en el inventario de la bodega.")
                elif cantidad > inventario.cantidad:
                    errores_stock.append(
                        f"Stock insuficiente para '{producto.nombre}'. Disponible: {inventario.cantidad}, solicitado: {cantidad}."
                    )

            if errores_stock:
                sweetify.error(
                    request,
                    title="Stock insuficiente",
                    text="\n".join(errores_stock),
                    timer=6000
                )
                return render(request, self.template_name, {
                    'form': form,
                    'productos': productos
                })

            # Guardar venta
            venta = form.save(commit=False)
            total = sum(Decimal(str(d['subtotal'])) for d in detalles)
            descuento = form.cleaned_data.get('descuento') or Decimal('0')
            venta.total = total * (Decimal('1') - (descuento / Decimal('100')))
            venta.save()

            for d in detalles:
                producto = d['producto']
                cantidad = d['cantidad']

                VentaDetalle.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=d['precio'],
                    subtotal=d['subtotal'],
                )

                inventario = InventarioBodega.objects.get(bodega=bodega, producto=producto)
                inventario.cantidad -= cantidad
                inventario.save()

            sweetify.success(
                request,
                title="¡Venta exitosa!",
                text="La venta se registró y el inventario se actualizó.",
                timer=3000
            )
            return redirect(self.success_url)

        sweetify.error(
            request,
            title="Error en el formulario",
            text="Por favor revisa los campos.",
            timer=3000
        )
        return render(request, self.template_name, {
            'form': form,
            'productos': productos
        })

    def _obtener_detalles_desde_post(self, post_data):
        productos = post_data.getlist('producto[]')
        cantidades = post_data.getlist('cantidad[]')
        precios = post_data.getlist('precio[]')
        subtotales = post_data.getlist('subtotal[]')

        detalles = []
        for i in range(len(productos)):
            try:
                producto = Producto.objects.get(pk=productos[i])
                cantidad = int(cantidades[i])
                precio = float(precios[i])
                subtotal = float(subtotales[i])
                if cantidad > 0 and precio >= 0:
                    detalles.append({
                        'producto': producto,
                        'cantidad': cantidad,
                        'precio': precio,
                        'subtotal': subtotal,
                    })
            except (Producto.DoesNotExist, ValueError):
                continue
        return detalles


class VentaUpdateView(LoginRequiredMixin, View):
    template_name = 'bonanza_ventas/venta_edit.html'
    success_url = reverse_lazy('ventas:venta_list')

    def get(self, request, pk, *args, **kwargs):
        venta = get_object_or_404(Venta, pk=pk)
        form = VentaForm(instance=venta)
        productos = Producto.objects.all()
        detalles_qs = VentaDetalle.objects.filter(venta=venta)

        detalles = []
        for d in detalles_qs:
            detalles.append({
                'producto_id': d.producto.id,
                'cantidad': d.cantidad,
                'precio': format(d.precio_unitario, '.2f'),
                'subtotal': format(d.subtotal, '.2f'),
            })
        print(detalles)
        return render(request, self.template_name, {
            'form': form,
            'productos': productos,
            'detalles': detalles,
            'venta': venta,
        })

    def post(self, request, pk, *args, **kwargs):
        venta = get_object_or_404(Venta, pk=pk)
        form = VentaForm(request.POST, instance=venta)
        productos = Producto.objects.all()
        detalles = self._obtener_detalles_desde_post(request.POST)

        if form.is_valid() and detalles:
            venta = form.save(commit=False)
            total = sum(Decimal(str(d['subtotal'])) for d in detalles)
            descuento = form.cleaned_data.get('descuento') or Decimal('0')
            venta.total = total * (Decimal('1') - (descuento / Decimal('100')))
            venta.save()

            VentaDetalle.objects.filter(venta=venta).delete()
            for d in detalles:
                VentaDetalle.objects.create(
                    venta=venta,
                    producto=d['producto'],
                    cantidad=d['cantidad'],
                    precio_unitario=d['precio'],
                    subtotal=d['subtotal'],
                )
            sweetify.success(
                request,
                title="¡Venta exitosa!",
                text="La venta fue actualizada correctamente.",
                persistent="ok"
            )
            return redirect(self.success_url)

        sweetify.error(
            request,
            title="Error en el formulario",
            text="Por favor revisa los campos e intenta de nuevo.",
            timer=3000
        )
        return render(request, self.template_name, {
            'form': form,
            'productos': productos,
            'venta': venta,
            'detalles': detalles,
        })

    def _obtener_detalles_desde_post(self, post_data):
        productos = post_data.getlist('producto')
        cantidades = post_data.getlist('cantidad')
        precios = post_data.getlist('precio')
        subtotales = post_data.getlist('subtotal')

        detalles = []
        for i in range(len(productos)):
            try:
                producto = Producto.objects.get(pk=productos[i])
                cantidad = int(cantidades[i])
                precio = float(precios[i])
                subtotal = float(subtotales[i])
                if cantidad > 0 and precio >= 0:
                    detalles.append({
                        'producto': producto,
                        'cantidad': cantidad,
                        'precio': precio,
                        'subtotal': subtotal,
                    })
            except (Producto.DoesNotExist, ValueError):
                continue
        return detalles

class VentaDeleteView(DeleteView):
    model = Venta
    template_name = 'bonanza_ventas/venta_confirm_delete.html'
    success_url = reverse_lazy('ventas:venta_list')

class VentaDetailView(DetailView):
    model = Venta
    template_name = 'bonanza_ventas/venta_detail.html'
    context_object_name = 'venta'