from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Municipio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Bodega(models.Model):
    nombre = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT, related_name='bodegas')

    def __str__(self):
        return f'{self.nombre} ({self.municipio})'

class InventarioBodega(models.Model):
    bodega = models.ForeignKey(Bodega, on_delete=models.PROTECT, related_name='inventario')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='inventarios')
    cantidad = models.PositiveIntegerField()
    cantidad_minima = models.PositiveIntegerField()

    class Meta:
        unique_together = ('bodega', 'producto')

    def __str__(self):
        return f'{self.producto} en {self.bodega}: {self.cantidad}'
