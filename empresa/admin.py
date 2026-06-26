from django.contrib import admin

from .models import EventoQR, Mascota, PlacaQR, Propietario, ReporteMascotaEncontrada


@admin.register(Propietario)
class PropietarioAdmin(admin.ModelAdmin):
    #list_display = ("id", "nombre", "email", "telefono", "estado", "fecha_registro")
    list_display = ("nombre", "email", "telefono", "mostrar_contacto_publico", "estado")
    search_fields = ("nombre", "email", "telefono")
    #list_filter = ("estado",)
    list_filter = ("mostrar_contacto_publico", "estado")


@admin.register(PlacaQR)
class PlacaQRAdmin(admin.ModelAdmin):
    list_display = ("codigo", "tipo_mascota", "estado", "activo", "fecha_generacion")
    list_filter = ("tipo_mascota", "estado", "activo")
    search_fields = ("codigo",)


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "tipo",
        "raza",
        "propietario",
        "placa_qr",
        "estado",
    )
    list_filter = ("tipo", "genero", "estado")
    search_fields = (
        "nombre",
        "raza",
        "placa_qr__codigo",
        "propietario__nombre",
    )


@admin.register(EventoQR)
class EventoQRAdmin(admin.ModelAdmin):
    list_display = ("id", "mascota", "propietario", "fecha_hora", "latitud", "longitud")
    list_filter = ("fecha_hora",)
    search_fields = ("mascota__nombre", "propietario__nombre")


#@admin.register(ReporteMascotaEncontrada)
#class ReporteMascotaEncontradaAdmin(admin.ModelAdmin):
#    list_display = ("id", "evento", "administrador", "fecha_reporte", "estado_reporte")
#    list_filter = ("estado_reporte", "fecha_reporte")
#    search_fields = ("evento__mascota__nombre", "mensaje")

@admin.register(ReporteMascotaEncontrada)
class ReporteMascotaEncontradaAdmin(admin.ModelAdmin):
     list_display = ("id","mascota","nombre_reportante","telefono_reportante","estado_reporte",
          "resultado_reporte", "fecha_reporte","fecha_cierre",)

     list_filter = ("estado_reporte","resultado_reporte","fecha_reporte","fecha_cierre",)

     search_fields = ("mascota__nombre","nombre_reportante","telefono_reportante",
           "mensaje","referencia_ubicacion","observaciones_cierre",)