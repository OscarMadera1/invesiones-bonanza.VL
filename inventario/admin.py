from django.contrib import admin
from .models import Municipio, Bodega, Categoria, Producto, InventarioBodega

admin.site.register(Municipio)
admin.site.register(Bodega)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(InventarioBodega)
