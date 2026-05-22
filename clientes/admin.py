from django.contrib import admin
from .models import Cliente, Servicio, Cita


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'email', 'telefono', 'activo', 'creado_en']
    list_filter = ['activo']
    search_fields = ['nombre', 'apellido', 'email']


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'duracion_minutos', 'precio', 'activo']
    list_filter = ['activo']


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'servicio', 'fecha', 'hora', 'estado']
    list_filter = ['estado', 'fecha']
    search_fields = ['cliente__nombre', 'cliente__apellido']
    date_hierarchy = 'fecha'
