# djangoProject

Proyecto escolar desarrollado con Django para registrar mascotas, propietarios y eventos asociados a códigos QR.

## Funcionalidades principales

- Registro de propietarios.
- Registro de mascotas.
- Asociación de mascotas con códigos QR.
- Consulta de detalles de cada mascota.
- Listado de mascotas y propietarios.
- Registro básico de eventos de ubicación mediante QR.
- Administración de datos desde Django Admin.

## Estructura general

```text
djangoProject/
├── manage.py
├── requirements.txt
├── djangoProject/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── empresa/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
└── templates/
    ├── base.html
    ├── login.html
    └── empresa/
        ├── inicio.html
        ├── servicios.html
        ├── contacto.html
        ├── admin_panel.html
        ├── registrar_mascota.html
        ├── listar_mascotas.html
        ├── listar_propietarios.html
        ├── detalles_mascota.html
        └── registrar_evento.html
```

## Requisitos

- Python 3.10 o superior
- PostgreSQL
- pip
- Entorno virtual recomendado

## Instalación local

1. Clonar el repositorio:

```bash
git clone https://github.com/luisleonanaya/djangoProject.git
cd djangoProject
```

2. Crear y activar un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

En Windows:

```bash
.venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Verificar la configuración de base de datos en `djangoProject/settings.py`.

Por defecto, el proyecto usa PostgreSQL con una base llamada `mascotas_db`.

5. Aplicar migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Crear un superusuario:

```bash
python manage.py createsuperuser
```

7. Ejecutar el servidor local:

```bash
python manage.py runserver
```

8. Abrir el proyecto en el navegador:

```text
http://127.0.0.1:8000/
```

## Rutas principales

- Inicio: `/`
- Servicios: `/servicios/`
- Contacto: `/contacto/`
- Registrar mascota: `/registrar-mascota/`
- Listar mascotas: `/listar-mascotas/`
- Listar propietarios: `/listar-propietarios/`
- Panel administrativo personalizado: `/admin-panel/`
- Django Admin: `/admin/`

## Notas

Este proyecto está pensado para ejecutarse localmente como proyecto escolar. No incluye configuración final para despliegue en Render u otro servicio de producción.
