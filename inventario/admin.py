from django.contrib import admin
from .models import Municipio, Empleado, Bodega, Producto, Inventario

admin.site.register(Municipio)
admin.site.register(Empleado)
admin.site.register(Bodega)
admin.site.register(Producto)
admin.site.register(Inventario)
