from django.urls import path
from . import views

app_name = 'bonanza_clientes'

urlpatterns = [
    path('', views.cliente_list, name='cliente_list'),
    path('nuevo/', views.cliente_create, name='cliente_create'),
    path('<int:pk>/editar/', views.cliente_update, name='cliente_update'),
    path('<int:pk>/eliminar/', views.cliente_delete, name='cliente_delete'),
]
