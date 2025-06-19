from django.db import models
from empleados.models import Empleado
from inventario.models import Municipio

class Zona(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    municipio = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    cobrador_asignado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True, related_name='zonas')

    def __str__(self):
        return f"{self.nombre} - {self.municipio}"
