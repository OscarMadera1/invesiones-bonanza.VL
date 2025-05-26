from django.urls import path
from . import views

urlpatterns = [
    path('', views.empleado_list, name='empleado_list'),
    path('crear/', views.empleado_create, name='empleado_create'),
    path('editar/<int:pk>/', views.empleado_update, name='empleado_update'),
    path('eliminar/<int:pk>/', views.empleado_delete, name='empleado_delete'),
]
