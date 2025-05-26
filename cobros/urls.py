from django.urls import path
from . import views

app_name = 'bonanza_cobros'

urlpatterns = [
    # Rutas de RutaCobro
    path('rutas/', views.RutaCobroListView.as_view(), name='ruta_list'),
    path('rutas/crear/', views.RutaCobroCreateView.as_view(), name='ruta_create'),
    path('rutas/editar/<int:pk>/', views.RutaCobroUpdateView.as_view(), name='ruta_update'),
    path('rutas/eliminar/<int:pk>/', views.RutaCobroDeleteView.as_view(), name='ruta_delete'),

    # Rutas de Cuota
    path('cuotas/', views.CuotaListView.as_view(), name='cuota_list'),
    path('cuotas/crear/', views.CuotaCreateView.as_view(), name='cuota_create'),
    path('cuotas/editar/<int:pk>/', views.CuotaUpdateView.as_view(), name='cuota_update'),
    path('cuotas/eliminar/<int:pk>/', views.CuotaDeleteView.as_view(), name='cuota_delete'),

    # Rutas de Pago
    path('pagos/', views.PagoListView.as_vi_
