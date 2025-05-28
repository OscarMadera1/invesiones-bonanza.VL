from django.db import models
from clientes.models import Cliente
from empleados.models import Empleado
from django.utils import timezone


class RutaCobro(models.Model):
    nombre = models.CharField(max_length=100)
    municipio = models.ForeignKey('inventario.Municipio', on_delete=models.CASCADE)
    zona = models.ForeignKey('clientes.ZonaCobro', on_delete=models.SET_NULL, null=True, blank=True)
    cobrador = models.ForeignKey(Empleado, on_delete=models.CASCADE, limit_choices_to={'rol': 'cobrador'})
    fecha_programada = models.DateField()

    def __str__(self):
        return f"{self.nombre} - {self.fecha_programada}"


class Cuota(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"Cuota de {self.cliente} - ${self.monto} - {'Pagado' if self.pagado else 'Pendiente'}"


class Pago(models.Model):
    cuota = models.ForeignKey(Cuota, on_delete=models.CASCADE)
    cobrador = models.ForeignKey(Empleado, on_delete=models.CASCADE, limit_choices_to={'rol': 'cobrador'})
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pago de ${self.monto_pagado} el {self.fecha_pago.date()}"

