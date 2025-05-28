from django.db import models

class ZonaCobro(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    identificacion = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    codeudor = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    zona = models.ForeignKey(ZonaCobro, on_delete=models.SET_NULL, null=True, related_name='clientes')
    municipio = models.ForeignKey('inventario.Municipio', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
