from django.db import models

class Municipio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    identificacion = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'
