from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/nuevo/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.cliente_edit, name='cliente_edit'),
    path('citas/', views.cita_list, name='cita_list'),
    path('citas/nueva/', views.cita_create, name='cita_create'),
    path('citas/<int:pk>/editar/', views.cita_edit, name='cita_edit'),
    path('calendario/', views.calendario, name='calendario'),
    path('api/citas/', views.citas_json, name='citas_json'),
    path('servicios/', views.servicio_list, name='servicio_list'),
    path('servicios/nuevo/', views.servicio_create, name='servicio_create'),
    path('servicios/<int:pk>/editar/', views.servicio_edit, name='servicio_edit'),
    path('servicios/<int:pk>/eliminar/', views.servicio_delete, name='servicio_delete'),
]
