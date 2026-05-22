from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import Cliente, Cita, Servicio
from .forms import ClienteForm, CitaForm, ServicioForm


@login_required
def dashboard(request):
    hoy = timezone.localdate()
    total_clientes = Cliente.objects.filter(activo=True).count()
    citas_hoy = Cita.objects.filter(fecha=hoy).count()
    citas_pendientes = Cita.objects.filter(estado='pendiente').count()
    citas_confirmadas = Cita.objects.filter(fecha=hoy, estado='confirmada').count()

    proximas_citas = Cita.objects.filter(
        fecha__gte=hoy,
        estado__in=['pendiente', 'confirmada']
    ).select_related('cliente', 'servicio').order_by('fecha', 'hora')[:8]

    context = {
        'total_clientes': total_clientes,
        'citas_hoy': citas_hoy,
        'citas_pendientes': citas_pendientes,
        'citas_confirmadas': citas_confirmadas,
        'proximas_citas': proximas_citas,
        'hoy': hoy,
    }
    return render(request, 'clientes/dashboard.html', context)


@login_required
def cliente_list(request):
    q = request.GET.get('q', '')
    clientes = Cliente.objects.filter(activo=True)
    if q:
        clientes = clientes.filter(
            Q(nombre__icontains=q) | Q(apellido__icontains=q) | Q(email__icontains=q)
        )
    return render(request, 'clientes/cliente_list.html', {'clientes': clientes, 'q': q})


@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nombre_completo}" registrado correctamente.')
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'clientes/cliente_form.html', {'form': form, 'titulo': 'Nuevo cliente'})


@login_required
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cliente "{cliente.nombre_completo}" actualizado.')
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/cliente_form.html', {'form': form, 'titulo': 'Editar cliente', 'cliente': cliente})


@login_required
def cita_list(request):
    estado = request.GET.get('estado', '')
    citas = Cita.objects.select_related('cliente', 'servicio').order_by('-fecha', '-hora')
    if estado:
        citas = citas.filter(estado=estado)
    return render(request, 'clientes/cita_list.html', {'citas': citas, 'estado': estado})


@login_required
def cita_create(request):
    initial = {}
    if request.GET.get('fecha'):
        initial['fecha'] = request.GET['fecha']
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.atendido_por = request.user
            cita.save()
            messages.success(request, f'Cita agendada para {cita.cliente.nombre_completo} el {cita.fecha}.')
            next_url = request.POST.get('next') or request.GET.get('next', 'cita_list')
            return redirect(next_url)
    else:
        form = CitaForm(initial=initial)
    return render(request, 'clientes/cita_form.html', {'form': form, 'titulo': 'Nueva cita'})


@login_required
def cita_edit(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada correctamente.')
            return redirect('cita_list')
    else:
        form = CitaForm(instance=cita)
    return render(request, 'clientes/cita_form.html', {'form': form, 'titulo': 'Editar cita', 'cita': cita})


@login_required
def calendario(request):
    form = CitaForm()
    return render(request, 'clientes/calendario.html', {'form': form})


@login_required
def citas_json(request):
    COLORES = {
        'pendiente':  '#f59e0b',
        'confirmada': '#10b981',
        'cancelada':  '#ef4444',
    }
    citas = Cita.objects.select_related('cliente', 'servicio').exclude(estado='cancelada')
    eventos = []
    for cita in citas:
        hora_str = cita.hora.strftime('%H:%M:%S')
        eventos.append({
            'id': cita.pk,
            'title': f"{cita.cliente.nombre_completo}{' · ' + cita.servicio.nombre if cita.servicio else ''}",
            'start': f"{cita.fecha}T{hora_str}",
            'color': COLORES.get(cita.estado, '#2563eb'),
            'extendedProps': {
                'estado': cita.get_estado_display(),
                'cliente': cita.cliente.nombre_completo,
                'servicio': cita.servicio.nombre if cita.servicio else '—',
                'notas': cita.notas,
                'edit_url': f'/citas/{cita.pk}/editar/',
            },
        })
    return JsonResponse(eventos, safe=False)


# ── Servicios ABM ──

@login_required
def servicio_list(request):
    servicios = Servicio.objects.all()
    return render(request, 'clientes/servicio_list.html', {'servicios': servicios})


@login_required
def servicio_create(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save()
            messages.success(request, f'Servicio "{servicio.nombre}" creado correctamente.')
            return redirect('servicio_list')
    else:
        form = ServicioForm()
    return render(request, 'clientes/servicio_form.html', {'form': form, 'titulo': 'Nuevo servicio'})


@login_required
def servicio_edit(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, f'Servicio "{servicio.nombre}" actualizado.')
            return redirect('servicio_list')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'clientes/servicio_form.html', {'form': form, 'titulo': 'Editar servicio', 'servicio': servicio})


@login_required
def servicio_delete(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        nombre = servicio.nombre
        servicio.delete()
        messages.success(request, f'Servicio "{nombre}" eliminado.')
    return redirect('servicio_list')
