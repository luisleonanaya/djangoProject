import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')  # Cambia 'djangoProject' al nombre de tu proyecto si es distinto
# Inicializa Django
django.setup()

from django.core.mail import send_mail

def enviar_correo_prueba():
    send_mail(
        'Asunto del correo',
        'Este es un segundo correo de prueba enviado desde Django usando Gmail SMTP.',
        'juanperezrosas007@gmail.com',  # Reemplaza con tu correo
        ['luisleonanaya@gmail.com'],  # Destinatario
        fail_silently=False,
    )

if __name__ == '__main__':
    enviar_correo_prueba()


