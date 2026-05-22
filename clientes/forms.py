from django import forms
from .models import Cliente, Cita, Servicio

# Horarios disponibles: 08:00 – 20:00 cada 30 minutos
_HORAS = [('', '— Selecciona una hora —')]
for _h in range(8, 21):
    for _m in (0, 30):
        if _h == 20 and _m == 30:
            break
        _t = f"{_h:02d}:{_m:02d}"
        _HORAS.append((_t, _t))


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'telefono', 'notas']
        widgets = {
            'nombre':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. García'}),
            'email':    forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 55 1234 5678'}),
            'notas':    forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Información adicional...'}),
        }
        labels = {
            'nombre':   'Nombre',
            'apellido': 'Apellido',
            'email':    'Correo electrónico',
            'telefono': 'Teléfono',
            'notas':    'Notas',
        }


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['cliente', 'servicio', 'fecha', 'hora', 'estado', 'notas']
        widgets = {
            'cliente':  forms.Select(attrs={'class': 'form-select'}),
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'fecha':    forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora':     forms.Select(choices=_HORAS, attrs={'class': 'form-select'}),
            'estado':   forms.Select(attrs={'class': 'form-select'}),
            'notas':    forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones...'}),
        }
        labels = {
            'cliente':  'Cliente',
            'servicio': 'Servicio',
            'fecha':    'Fecha',
            'hora':     'Hora',
            'estado':   'Estado',
            'notas':    'Notas',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.filter(activo=True).order_by('apellido', 'nombre')
        self.fields['servicio'].queryset = Servicio.objects.filter(activo=True)
        self.fields['servicio'].required = False
        self.fields['servicio'].empty_label = '— Sin servicio —'


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'duracion_minutos', 'precio', 'activo']
        widgets = {
            'nombre':           forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Consulta general'}),
            'descripcion':      forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del servicio...'}),
            'duracion_minutos': forms.NumberInput(attrs={'class': 'form-control', 'min': 15, 'step': 15}),
            'precio':           forms.TextInput(attrs={'class': 'form-control precio-gs', 'placeholder': '0', 'inputmode': 'numeric'}),
            'activo':           forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre':           'Nombre del servicio',
            'descripcion':      'Descripción',
            'duracion_minutos': 'Duración (minutos)',
            'precio':           'Precio (Gs)',
            'activo':           'Servicio activo',
        }

    def clean_precio(self):
        value = self.cleaned_data.get('precio', '')
        cleaned = str(value).replace('.', '').replace(',', '').strip()
        if not cleaned:
            return 0
        try:
            return int(cleaned)
        except ValueError:
            raise forms.ValidationError('Ingresa un monto válido.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.precio:
            formatted = f"{instance.precio:,}".replace(',', '.')
            self.initial['precio'] = formatted
