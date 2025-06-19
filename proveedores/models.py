from django.db import models

class Proveedor(models.Model):
    codigo = models.IntegerField(max_length=20, unique=True)
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    telefono = models.IntegerField(max_length=15)

    def __str__(self):
        return f"{self.nombre}"

