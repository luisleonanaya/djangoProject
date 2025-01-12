from django.urls import path
from . import views  # Importa las vistas de la misma aplicación
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Ruta para la página de inicio
    path('servicios/', views.servicios, name='servicios'),  # Ruta para la página de servicios
    path('contacto/', views.contacto, name='contacto'),  # Ruta para la página de contacto
    path('admin-panel/', views.admin_panel, name='admin_panel'),  # Ruta para el panel de administración
    path('mascota/<uuid:mascota_id>/', views.detalles_mascota, name='detalles_mascota'), # Detalles de mascota
    path('mascota/<int:mascota_id>/guardar-ubicacion/', views.guardar_ubicacion, name='guardar_ubicacion'),  # Guardar ubicación
    path('borrar-mascota/<uuid:id>/', views.borrar_mascota, name='borrar_mascota'),  # Borrar mascota
    path('eliminar-propietario/<int:propietario_id>/', views.eliminar_propietario, name='eliminar_propietario'), # Borrar propietario
    path('mascota/<uuid:id>/registrar-evento/', views.registrar_evento_qr, name='registrar_evento_qr'),  # Registrar evento QR
    path('registrar-mascota/', views.registrar_mascota, name='registrar_mascota'),  # Registrar mascota
    path('listar-mascotas/', views.listar_mascotas, name='listar_mascotas'),  # Listar mascotas
    path('listar-propietarios/', views.listar_propietarios, name='listar_propietarios'),  # Listar propietarios
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



