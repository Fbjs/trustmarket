from django.db import models


class Application(models.Model):
    EXPERIENCE_CHOICES = [
        ("sin_experiencia", "No"),
        ("menos_1", "< 1 año"),
        ("1_3", "1-3 años"),
        ("mas_3", "+3 años"),
    ]

    full_name = models.CharField("Nombre completo", max_length=160)
    phone = models.CharField("Teléfono / WhatsApp", max_length=30)
    email = models.EmailField("Correo electrónico")
    age = models.PositiveSmallIntegerField("Edad")
    sales_experience = models.CharField(
        "Experiencia en ventas", max_length=20, choices=EXPERIENCE_CHOICES
    )
    availability = models.TextField("Disponibilidad")
    additional_comments = models.TextField("Comentarios adicionales", blank=True)
    created_at = models.DateTimeField("Fecha de postulación", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Postulación"
        verbose_name_plural = "Postulaciones"

    def __str__(self) -> str:
        return f"{self.full_name} - {self.created_at:%d/%m/%Y}"


class postulaciones(models.Model):
    # Django necesita que marques managed = False para no alterar tu tabla manual
    id = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=255)
    telefono = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    edad = models.IntegerField()
    experiencia_ventas = models.CharField(max_length=100)
    disponibilidad = models.TextField() # Aquí guardaremos los checkboxes como texto
    comentarios = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # NO toca la estructura de la tabla manual
        db_table = 'postulaciones' # Nombre exacto en MySQL

class StitchApplication(models.Model):
    EXPERIENCE_CHOICES = [
        ("sin_experiencia", "Sin experiencia"),
        ("1_2", "1-2 años"),
        ("mas_3", "3+ años"),
    ]

    full_name = models.CharField("Nombre completo", max_length=160)
    email = models.EmailField("Correo electrónico")
    phone = models.CharField("Teléfono", max_length=30)
    experience = models.CharField(
        "Experiencia (Años)", max_length=20, choices=EXPERIENCE_CHOICES
    )
    cv = models.FileField("Adjuntar CV (PDF)", upload_to="cvs/")
    created_at = models.DateTimeField("Fecha de postulación", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Postulación"
        verbose_name_plural = "Postulaciones"

    def __str__(self) -> str:
        return f"{self.full_name} - {self.created_at:%d/%m/%Y}"