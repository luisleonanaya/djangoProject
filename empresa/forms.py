from django import forms
from .models import Propietario, Mascota
from .models import EventoQR
from django.forms.widgets import DateInput

class EventoQRForm(forms.ModelForm):
    class Meta:
        model = EventoQR
        fields = ['mascota', 'propietario', 'latitud', 'longitud', 'notas']



class PropietarioForm(forms.ModelForm):
    class Meta:
        model = Propietario
        fields = ['nombre', 'email', 'telefono', 'direccion']

class MascotaForm(forms.ModelForm):
    codigo_qr = forms.ChoiceField(
        label="Selecciona un Código QR",
        choices=[],  # Opciones dinámicas
        required=True
    )

    class Meta:
        model = Mascota
        fields = ['nombre', 'tipo', 'raza', 'fecha_nacimiento', 'genero', 'estado_salud', 'descripcion', 'foto']
        widgets = {
            'fecha_nacimiento': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar códigos QR no asignados
        self.fields['codigo_qr'].choices = [
            (m.codigo_qr, m.codigo_qr) for m in Mascota.objects.filter(nombre__isnull=True)
        ]