from django.db import models
from empleados.models import Empleado
from inventario.models import Municipio, Bodega

class Zona(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    municipio = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    cobrador_asignado = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name='zonas')
    bodega = models.ForeignKey(Bodega, on_delete=models.PROTECT, related_name='zonas')

    def __str__(self):
        return f"{self.nombre} - {self.municipio}"
