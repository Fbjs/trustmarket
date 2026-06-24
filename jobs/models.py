import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models


def validate_chilean_phone(value):
    if not value:
        return
    cleaned = re.sub(r'[\s\-\(\)\.]', '', value)
    pattern = re.compile(r'^(\+?56)?([2-9]\d{8})$')
    if not pattern.match(cleaned):
        raise ValidationError(
            _("El número de teléfono no es válido para Chile. Debe tener 9 dígitos (ej: 9 1234 5678 o +56 9 1234 5678).")
        )


def normalize_chilean_phone(value):
    if not value:
        return value
    cleaned = re.sub(r'[\s\-\(\)\.]', '', value)
    pattern = re.compile(r'^(\+?56)?([2-9]\d{8})$')
    match = pattern.match(cleaned)
    if match:
        national_number = match.group(2)
        if national_number.startswith('9'):
            return f"+56 9 {national_number[1:5]} {national_number[5:]}"
        elif national_number.startswith('2'):
            return f"+56 2 {national_number[1:5]} {national_number[5:]}"
        else:
            return f"+56 {national_number[0:2]} {national_number[2:5]} {national_number[5:]}"
    return value


class Application(models.Model):
    EXPERIENCE_CHOICES = [
        ("sin_experiencia", "No"),
        ("menos_1", "< 1 año"),
        ("1_3", "1-3 años"),
        ("mas_3", "+3 años"),
    ]

    POSITION_CHOICES = [
        ("ejecutivo_ventas", "Ejecutivo de Ventas de Seguros"),
        ("ejecutivo_encuestas", "Ejecutivo de Encuestas"),
        ("atencion_cliente", "Atención al Cliente"),
        ("soporte_comercial", "Soporte Comercial"),
        ("supervisor", "Supervisor de Ventas"),
    ]

    full_name = models.CharField("Nombre completo", max_length=160)
    phone = models.CharField("Teléfono / WhatsApp", max_length=30, validators=[validate_chilean_phone])
    email = models.EmailField("Correo electrónico")
    age = models.PositiveSmallIntegerField("Edad")
    position = models.CharField(
        "Puesto al que postula", max_length=50, choices=POSITION_CHOICES, default="ejecutivo_ventas"
    )
    sales_experience = models.CharField(
        "Experiencia en ventas", max_length=20, choices=EXPERIENCE_CHOICES, default="sin_experiencia"
    )
    availability = models.TextField("Disponibilidad", blank=True)
    cv = models.FileField("CV", upload_to="cvs/", null=True, blank=True)
    additional_comments = models.TextField("Comentarios adicionales", blank=True)
    equipamiento_audio = models.CharField("Equipamiento de audio", max_length=50, blank=True, null=True)
    especificaciones_pc = models.CharField("Especificaciones de PC", max_length=20, blank=True, null=True)
    conexion = models.CharField("Conexión", max_length=20, blank=True, null=True)
    competencias = models.CharField("Competencias", max_length=20, blank=True, null=True)
    ESTADO_CHOICES = [
        ("Postulando", "Postulando"),
        ("Califica", "Califica"),
        ("No califica", "No califica"),
        ("Contactado", "Contactado"),
        ("Volver a llamar", "Volver a llamar"),
        ("Seguna etapa", "Seguna etapa"),
        ("Contratado", "Contratado"),
        ("Desvinculado", "Desvinculado"),
        ("Abandono", "Abandono"),
    ]

    estado = models.CharField(
        "Estado", max_length=40, choices=ESTADO_CHOICES, default="Postulando"
    )
    observaciones = models.CharField(
        "Observaciones", max_length=200, blank=True, default=""
    )
    created_at = models.DateTimeField("Fecha de postulación", auto_now_add=True)


    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Postulación"
        verbose_name_plural = "Postulaciones"

    def __str__(self) -> str:
        return f"{self.full_name} - {self.created_at:%d/%m/%Y}"

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = normalize_chilean_phone(self.phone)
        super().save(*args, **kwargs)


class postulaciones(models.Model):
    # Django necesita que marques managed = False para no alterar tu tabla manual
    id = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=255)
    telefono = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    edad = models.IntegerField()
    puesto = models.CharField(max_length=100, blank=True, null=True)
    experiencia_ventas = models.CharField(max_length=100)
    disponibilidad = models.TextField() # Aquí guardaremos los checkboxes como texto
    cv_url = models.CharField(max_length=500, blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
    equipamiento_audio = models.CharField(max_length=50, blank=True, null=True)
    especificaciones_pc = models.CharField(max_length=20, blank=True, null=True)
    conexion = models.CharField(max_length=20, blank=True, null=True)
    competencias = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False  # NO toca la estructura de la tabla manual
        db_table = 'postulaciones' # Nombre exacto en MySQL


class CompanyLead(models.Model):
    COMPANY_SIZE_CHOICES = [
        ("1_10", "1-10 colaboradores"),
        ("11_50", "11-50 colaboradores"),
        ("51_200", "51-200 colaboradores"),
        ("200_mas", "200+ colaboradores"),
    ]

    SERVICE_CHOICES = [
        ("ventas_seguros", "Venta de seguros de salud"),
        ("atencion_cliente", "Atencion al cliente"),
        ("soporte_comercial", "Soporte comercial"),
        ("outsourcing", "Outsourcing de equipos"),
        ("otro", "Otro"),
    ]

    company_name = models.CharField("Empresa", max_length=180)
    contact_name = models.CharField("Nombre de contacto", max_length=160)
    email = models.EmailField("Correo corporativo")
    phone = models.CharField("Telefono / WhatsApp", max_length=30, validators=[validate_chilean_phone])
    company_size = models.CharField("Tamano de empresa", max_length=20, choices=COMPANY_SIZE_CHOICES)
    service_interest = models.CharField("Servicio de interes", max_length=40, choices=SERVICE_CHOICES)
    message = models.TextField("Necesidad o mensaje", blank=True)
    created_at = models.DateTimeField("Fecha de contacto", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contacto empresa"
        verbose_name_plural = "Contactos empresas"

    def __str__(self) -> str:
        return f"{self.company_name} - {self.contact_name}"

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = normalize_chilean_phone(self.phone)
        super().save(*args, **kwargs)
