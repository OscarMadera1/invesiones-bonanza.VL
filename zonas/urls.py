from django.urls import path
from . import views

app_name = 'zonas'

urlpatterns = [
    path('', views.lista_zonas, name='lista_zonas'),
    path('crear/', views.crear_zona, name='crear_zona'),
    path('editar/<int:zona_id>/', views.editar_zona, name='editar_zona'),
    path('eliminar/<int:zona_id>/', views.eliminar_zona, name='eliminar_zona'),
]
