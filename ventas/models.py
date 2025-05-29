from django.db import models
from clientes.models import Cliente
from empleados.models import Empleado
from inventario.models import Producto


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ventas')
    vendedor = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='ventas_realizadas')
    fecha_venta = models.DateTimeField(auto_now_add=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('finalizada', 'Finalizada'),
                                                      ('cancelada', 'Cancelada')], default='pendiente')

    def __str__(self):
        return f"Venta #{self.id} - Cliente: {self.cliente} - Total: {self.total}"


class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad} (Venta #{self.venta.id})"
