# 🚀 TrustMarket Web Redesign + Módulo de Postulación

## 📌 Descripción del Proyecto

Este proyecto tiene como objetivo el **rediseño completo del sitio web de TrustMarket** y la **implementación de un módulo de postulación integrado**, orientado a la captación de candidatos para el call center (venta de seguros de salud).

El sistema permitirá mejorar la presencia digital de la empresa y funcionar como una **herramienta de reclutamiento automatizado**, capturando y gestionando postulantes de forma eficiente.

---

## 🎯 Objetivos

* Rediseñar la página web actual con enfoque moderno y orientado a conversión.
* Integrar una sección **“Trabaja con Nosotros”** dentro del sitio.
* Implementar un formulario de postulación con almacenamiento de datos.
* Permitir notificaciones automáticas de nuevos postulantes.
* Mantener control de versiones mediante Git.

---

## 🧱 Alcance del Proyecto

### Incluye:

* Rediseño UX/UI del sitio completo
* Desarrollo frontend responsive
* Desarrollo backend (captura de postulantes)
* Integración de base de datos
* Sistema de notificaciones (email / futuro WhatsApp)
* Deploy en entorno productivo

### No incluye (fase actual):

* Integración completa con CRM (Fénix) *(fase futura)*
* Automatización avanzada de contacto *(fase futura)*

---

## 🗺️ Estructura del Sitio

* Inicio
* Servicios
* Sobre Nosotros
* **Trabaja con Nosotros**
* Contacto

---

## 🧑‍💼 Módulo de Postulación

El sistema permitirá capturar información de candidatos interesados en trabajar en el call center.

### 📥 Datos capturados:

* Nombre completo
* Teléfono (WhatsApp)
* Email
* Edad
* Experiencia en ventas
* Disponibilidad
* Comentarios adicionales

### ⚙️ Flujo:

1. Usuario accede a la sección “Trabaja con Nosotros”
2. Completa el formulario
3. Se validan los datos
4. Se almacenan en la base de datos
5. Se genera notificación al equipo

---

## 🏗️ Arquitectura General

```
Frontend (Sitio Web)
   ↓
Formulario de Postulación
   ↓
Backend / API
   ↓
Base de Datos
   ↓
Notificaciones (Email / WhatsApp - futuro)
```

---

## 🛠️ Stack Tecnológico (definir según implementación)

* Frontend: Astro / HTML / TailwindCSS
* Backend: Laravel / Node.js / Firebase
* Base de datos: MySQL / Firestore
* Control de versiones: Git

---

## 📅 Plan de Trabajo (3 semanas)

### 🟢 Semana 1 – Análisis y Base del Proyecto

* Auditoría de la web actual
* Definición de estructura del sitio
* Definición del flujo de postulación
* Setup del entorno de desarrollo

---

### 🟡 Semana 2 – Desarrollo

* Implementación del rediseño frontend
* Desarrollo de la sección “Trabaja con Nosotros”
* Construcción del formulario de postulación
* Implementación de backend y almacenamiento
* Validaciones y pruebas iniciales

---

### 🔵 Semana 3 – Optimización y Publicación

* Optimización responsive
* Mejora de UX/UI
* Integración de tracking (Analytics / Pixel)
* Configuración de dominio y SSL
* Deploy en producción
* Pruebas finales

---

## 🔔 Funcionalidades Clave

* Captura de leads (postulantes)
* Validación de datos
* Persistencia en base de datos
* Notificación automática de nuevos registros
* Diseño optimizado para conversión

---

## 📊 Futuras Mejoras

* Integración con CRM Fénix
* Automatización de contacto vía WhatsApp
* Panel de administración de postulantes
* Sistema de scoring de candidatos

---

## ⚠️ Consideraciones Importantes

* El enfoque principal del sitio es **reclutamiento**, no solo informativo.
* El formulario debe ser **rápido y simple** (alta conversión).
* El botón **“Trabaja con Nosotros”** debe ser visible en todo momento.
* Todo el desarrollo debe quedar versionado en Git.

---

## 👨‍💻 Flujo de Trabajo Git (recomendado)

* `main` → Producción
* `develop` → Desarrollo
* `feature/*` → Nuevas funcionalidades

Ejemplo:

```
feature/redesign-home
feature/form-postulacion
feature/backend-leads
```

---

## 🚀 Estado del Proyecto

🟡 En desarrollo

---

## 📞 Contacto

Proyecto desarrollado para TrustMarket.

---
