from django.urls import path
from .views import (
    VentaListView,
    VentaCreateView,
    VentaUpdateView,
    VentaDeleteView,
    VentaDetailView,
    MapaVentasView,
)

app_name = 'ventas'

urlpatterns = [
    path('', VentaListView.as_view(), name='venta_list'),
    path('crear/', VentaCreateView.as_view(), name='venta_crear'),
    path('editar/<int:pk>/', VentaUpdateView.as_view(), name='venta_editar'),
    path('eliminar/<int:pk>/', VentaDeleteView.as_view(), name='venta_eliminar'),
    path('detalle/<int:pk>/', VentaDetailView.as_view(), name='venta_detalle'),
    path('mapa/', MapaVentasView.as_view(), name='mapa_ventas'),
]