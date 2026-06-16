import json
import os

import qrcode
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from io import BytesIO

from .forms import EventoQRForm, GenerarPlacasQRForm, MascotaForm, PropietarioForm
from .models import EventoQR, Mascota, PlacaQR, Propietario


def inicio(request):
    return render(request, "empresa/inicio.html")


def servicios(request):
    return render(request, "empresa/servicios.html")


def contacto(request):
    if request.method == "POST":
        messages.success(request, "Mensaje recibido correctamente.")
        return redirect("contacto")

    return render(request, "empresa/contacto.html")


@login_required
def admin_panel(request):
    return render(request, "empresa/admin_panel.html")


def listar_propietarios(request):
    propietarios = Propietario.objects.all().order_by("nombre")
    return render(
        request,
        "empresa/listar_propietarios.html",
        {"propietarios": propietarios},
    )


@require_POST
def eliminar_propietario(request, propietario_id):
    propietario = get_object_or_404(Propietario, id=propietario_id)
    propietario.delete()
    messages.success(request, "Propietario eliminado correctamente.")
    return redirect("listar_propietarios")

def registrar_mascota(request):
    if request.method == "POST":
        propietario_form = PropietarioForm(request.POST)
        mascota_form = MascotaForm(request.POST, request.FILES)

        if propietario_form.is_valid() and mascota_form.is_valid():
            propietario = propietario_form.save()
            placa_qr = mascota_form.cleaned_data["placa_qr"]

            mascota = Mascota.objects.create(
                propietario=propietario,
                placa_qr=placa_qr,
                nombre=mascota_form.cleaned_data["nombre"],
                tipo=mascota_form.cleaned_data["tipo"],
                raza=mascota_form.cleaned_data["raza"],
                fecha_nacimiento=mascota_form.cleaned_data["fecha_nacimiento"],
                genero=mascota_form.cleaned_data["genero"],
                color=mascota_form.cleaned_data["color"],
                estado_salud=mascota_form.cleaned_data["estado_salud"],
                senas_particulares=mascota_form.cleaned_data["senas_particulares"],
                descripcion=mascota_form.cleaned_data["descripcion"],
                foto=mascota_form.cleaned_data["foto"],
            )

            placa_qr.estado = "Asignada"
            placa_qr.save()

            messages.success(
                request,
                f"Mascota {mascota.nombre} registrada correctamente con la placa {placa_qr.codigo}."
            )
            return redirect("listar_mascotas")
    else:
        propietario_form = PropietarioForm()
        mascota_form = MascotaForm()

    return render(
        request,
        "empresa/registrar_mascota.html",
        {
            "propietario_form": propietario_form,
            "mascota_form": mascota_form,
        },
    )

def listar_mascotas(request):
    mascotas = Mascota.objects.select_related("propietario").all().order_by("nombre")
    return render(request, "empresa/listar_mascotas.html", {"mascotas": mascotas})


@require_POST
def borrar_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    mascota.delete()
    messages.success(request, "Mascota eliminada correctamente.")
    return redirect("listar_mascotas")


def registrar_evento(request):
    if request.method == "POST":
        form = EventoQRForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento registrado correctamente.")
            return redirect("inicio")
    else:
        form = EventoQRForm()

    return render(request, "empresa/registrar_evento.html", {"form": form})


def registrar_evento_qr(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    propietario = mascota.propietario
    latitud = request.GET.get("latitud")
    longitud = request.GET.get("longitud")

    if not propietario:
        return JsonResponse(
            {"error": "La mascota no tiene propietario asignado."},
            status=400,
        )

    if not latitud or not longitud:
        return JsonResponse(
            {"error": "No se proporcionaron coordenadas."},
            status=400,
        )

    EventoQR.objects.create(
        mascota=mascota,
        propietario=propietario,
        latitud=latitud,
        longitud=longitud,
    )

    qr_url = generar_qr_mascota(request, mascota)
    return render(
        request,
        "empresa/detalles_mascota.html",
        {
            "mascota": mascota,
            "qr_url": qr_url,
            "latitud": latitud,
            "longitud": longitud,
        },
    )


@csrf_exempt
@require_POST
def guardar_ubicacion(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    try:
        datos = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido."}, status=400)

    latitud = datos.get("latitud")
    longitud = datos.get("longitud")

    if not latitud or not longitud:
        return JsonResponse(
            {"error": "Latitud y longitud son obligatorias."},
            status=400,
        )

    evento = None
    if mascota.propietario:
        evento = EventoQR.objects.create(
            mascota=mascota,
            propietario=mascota.propietario,
            latitud=latitud,
            longitud=longitud,
        )

    return JsonResponse(
        {
            "mensaje": "Ubicación guardada correctamente.",
            "evento_id": evento.id if evento else None,
        },
        status=200,
    )


def detalles_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    latitud = request.GET.get("lat")
    longitud = request.GET.get("lon")
    qr_url = generar_qr_mascota(request, mascota)

    context = {
        "mascota": mascota,
        "qr_url": qr_url,
        "latitud": latitud,
        "longitud": longitud,
    }
    return render(request, "empresa/detalles_mascota.html", context)


def generar_qr_mascota(request, mascota):
    detalles_url = request.build_absolute_uri(
        reverse("detalles_mascota", args=[mascota.id])
    )
    url_con_parametros = f"{detalles_url}?lat={{lat}}&lon={{lon}}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url_con_parametros)
    qr.make(fit=True)

    qr_dir = os.path.join(settings.MEDIA_ROOT, "qr_codes")
    os.makedirs(qr_dir, exist_ok=True)

    qr_filename = f"{mascota.id}.png"
    qr_path = os.path.join(qr_dir, qr_filename)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_path)

    return f"{settings.MEDIA_URL}qr_codes/{qr_filename}"

def placas_disponibles_por_tipo(request):
    tipo = request.GET.get("tipo")

    placas = []

    if tipo in ["Perro", "Gato", "Otro"]:
        placas_qr = PlacaQR.objects.filter(
            tipo_mascota=tipo,
            estado="Disponible",
            activo=True
        ).order_by("codigo")

        placas = [
            {
                "id": str(placa.id),
                "codigo": placa.codigo,
                "tipo_mascota": placa.tipo_mascota,
            }
            for placa in placas_qr
        ]

    return JsonResponse({"placas": placas})

@login_required
def generar_placas_qr(request):
    if request.method == "POST":
        form = GenerarPlacasQRForm(request.POST)

        if form.is_valid():
            tipo_mascota = form.cleaned_data["tipo_mascota"]
            cantidad = form.cleaned_data["cantidad"]

            placas_creadas = []

            for _ in range(cantidad):
                placa = PlacaQR.objects.create(
                    tipo_mascota=tipo_mascota,
                    estado="Disponible",
                    activo=True,
                )
                placas_creadas.append(placa)

            messages.success(
                request,
                f"Se generaron {len(placas_creadas)} placas QR para {tipo_mascota}."
            )
            return redirect("listar_placas_qr")
    else:
        form = GenerarPlacasQRForm()

    return render(
        request,
        "empresa/generar_placas_qr.html",
        {"form": form},
    )


@login_required
def listar_placas_qr(request):
    placas = PlacaQR.objects.all().order_by("-fecha_generacion")

    return render(
        request,
        "empresa/listar_placas_qr.html",
        {"placas": placas},
    )


def detalle_placa_qr(request, placa_id):
    placa = get_object_or_404(PlacaQR, id=placa_id, activo=True)

    try:
        mascota = placa.mascota
        return redirect("detalles_mascota", mascota_id=mascota.id)
    except Mascota.DoesNotExist:
        return render(
            request,
            "empresa/placa_sin_asignar.html",
            {"placa": placa},
        )


@login_required
def ver_qr_placa(request, placa_id):
    placa = get_object_or_404(PlacaQR, id=placa_id)

    url_placa = request.build_absolute_uri(
        reverse("detalle_placa_qr", args=[placa.id])
    )

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url_placa)
    qr.make(fit=True)

    imagen = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    imagen.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")

@login_required
def descargar_qr_placa(request, placa_id):
    placa = get_object_or_404(PlacaQR, id=placa_id)

    url_placa = request.build_absolute_uri(
        reverse("detalle_placa_qr", args=[placa.id])
    )

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url_placa)
    qr.make(fit=True)

    imagen = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    imagen.save(buffer, format="PNG")
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    response["Content-Disposition"] = f'attachment; filename="{placa.codigo}.png"'
    return response

@login_required
def imprimir_placas_qr(request):
    placas = PlacaQR.objects.filter(
        activo=True
    ).order_by("tipo_mascota", "codigo")

    return render(
        request,
        "empresa/imprimir_placas_qr.html",
        {"placas": placas},
    )