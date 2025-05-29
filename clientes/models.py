from django.db import models

class Cliente(models.Model):
    identificacion = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    codeudor = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    zona = models.ForeignKey('zonas.Zona', on_delete=models.SET_NULL, null=True)
    municipio = models.ForeignKey('inventario.Municipio', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
