from django.contrib import admin
from .models import Producto, Categoria, Municipio, Bodega, InventarioBodega

admin.site.register(Municipio)
admin.site.register(InventarioBodega)
admin.site.register(Bodega)
admin.site.register(Producto)
admin.site.register(Categoria)
