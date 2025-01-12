from django.db import models
import uuid
from django.utils.timezone import now

class Propietario(models.Model):
    id = models.AutoField(primary_key=True)  # AUTO_INCREMENT en SQL
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Mascota(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    propietario = models.ForeignKey(
        'Propietario',
        on_delete=models.CASCADE,
        related_name='mascotas',
        null=True,  # Permite valores nulos
        blank=True  # Permite que el campo sea opcional en formularios
    )
    nombre = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.CharField(
        max_length=50, choices=[('Perro', 'Perro'), ('Gato', 'Gato'), ('Conejo', 'Conejo')], null=True, blank=True
    )
    raza = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    genero = models.CharField(
        max_length=10, choices=[('Macho', 'Macho'), ('Hembra', 'Hembra')], null=True, blank=True
    )
    estado_salud = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='mascotas/', blank=True, null=True)
    codigo_qr = models.CharField(max_length=255, unique=True, blank=False, null=False)

    def __str__(self):
        return self.codigo_qr


class EventoQR(models.Model):
    id = models.AutoField(primary_key=True)  # ID autoincremental para el evento
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='eventos')
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='eventos')
    fecha_hora = models.DateTimeField(default=now)  # Fecha y hora del evento
    latitud = models.FloatField(blank=True, null=True)  # Latitud (-90 a 90)
    longitud = models.FloatField(blank=True, null=True)  # Longitud (-180 a 180)
    notas = models.TextField(blank=True, null=True)  # Notas adicionales (opcional)

    def __str__(self):
        return f"Evento {self.id} - Mascota: {self.mascota.nombre} - Propietario: {self.propietario.nombre}"


