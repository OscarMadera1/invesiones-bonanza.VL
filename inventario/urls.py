from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Productos
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),

    # Categorías
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),

    # Municipios
    path('municipios/', views.lista_municipios, name='lista_municipios'),
    path('municipios/crear/', views.crear_municipio, name='crear_municipio'),
    path('municipios/editar/<int:municipio_id>/', views.editar_municipio, name='editar_municipio'),
    path('municipios/eliminar/<int:municipio_id>/', views.eliminar_municipio, name='eliminar_municipio'),

    # Bodegas
    path('bodegas/', views.lista_bodegas, name='lista_bodegas'),
    path('bodegas/crear/', views.crear_bodega, name='crear_bodega'),
    path('bodegas/editar/<int:bodega_id>/', views.editar_bodega, name='editar_bodega'),
    path('bodegas/eliminar/<int:bodega_id>/', views.eliminar_bodega, name='eliminar_bodega'),

    # Inventario por bodega
    path('bodegas/<int:bodega_id>/inventario/', views.inventario_bodega, name='inventario_bodega'),
    path('bodegas/<int:bodega_id>/inventario/crear/', views.crear_inventario_bodega, name='crear_inventario_bodega'),
    path('bodegas/<int:bodega_id>/inventario/editar/<int:item_id>/', views.editar_inventario_bodega, name='editar_inventario_bodega'),
    path('bodegas/<int:bodega_id>/inventario/eliminar/<int:item_id>/', views.eliminar_inventario_bodega, name='eliminar_inventario_bodega'),
]
