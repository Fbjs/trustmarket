# TrustMarket Web Redesign (Django)

Rediseño corporativo moderno para TrustMarket y módulo de postulación integrado para reclutamiento de ejecutivos de call center.

## Características principales

- Sitio corporativo con páginas de Inicio, Servicios, Quiénes Somos y Contacto.
- Módulo de postulación en `/trabaja-con-nosotros/`.
- Gestión de postulantes desde Django Admin.
- Envío de correos por consola en entorno local.
- **Base de datos SQLite por defecto**, lista para usar al clonar.
- **Soporte opcional para MySQL** mediante variables de entorno.

## Requisitos previos

- Python 3.12+ (recomendado)
- Git
- (Opcional) MySQL Server si quieres usar MySQL en lugar de SQLite

## Puesta en marcha (Windows)

1. **Clonar el repositorio**

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd Trust-MK-prueba
   ```

2. **Crear entorno virtual**

   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**

   ```bash
   venv\Scripts\activate
   ```

4. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecutar migraciones**

   ```bash
   python manage.py migrate
   ```

6. **Levantar servidor**

   ```bash
   python manage.py runserver
   ```

7. Abrir en el navegador: `http://127.0.0.1:8000/`

## Base de datos por defecto (SQLite)

Este proyecto está configurado para usar **SQLite por defecto** en desarrollo local.

Si no defines `USE_MYSQL=True`, Django usará automáticamente el archivo local `db.sqlite3`, por lo que **no necesitas instalar MySQL para ejecutar el proyecto** en una máquina nueva.

## Usar MySQL de forma opcional

Si quieres trabajar con MySQL, crea un archivo `.env` en la raíz del proyecto basado en `.env.example`:

```env
USE_MYSQL=True
DB_NAME=trustmarket
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Con esa configuración, el proyecto cambiará de SQLite a MySQL automáticamente.

## Archivo de referencia de entorno

Se incluye `.env.example` con la configuración base:

```env
USE_MYSQL=False

DB_NAME=trustmarket
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
```

## Flujo visual implementado

- Header sticky con branding TrustMarket.
- Hero principal en Inicio.
- Landing independiente para cada opción del menú:
  - Inicio (`/`)
  - Servicios (`/servicios/`)
  - Quiénes Somos (`/quienes-somos/`)
  - Contacto (`/contacto/`)
- Footer corporativo con navegación rápida.

## Módulo de Postulación

- URL dedicada: `/trabaja-con-nosotros/`
- **Integración de WhatsApp**: Notificación automática al postulante vía API oficial de Meta (a través de `call.neighbour.cl`).
- Stepper visual: "Tus Datos" → "Experiencia" → "Disponibilidad".
- Validaciones de campos obligatorios y edad mínima.
- Guardado en base de datos (`Application`).
- **Doble guardado manual**: Guarda simultáneamente en tabla `postulaciones` externa (si se usa MySQL, se *debe* tener la columna `puesto` creada de forma manual usando `ALTER TABLE postulaciones ADD COLUMN puesto VARCHAR(100) NULL;`).
- Notificación automática por correo (backend consola en desarrollo) con recepción de datos del puesto al que postula.
- Gestión de postulantes en Django Admin.
