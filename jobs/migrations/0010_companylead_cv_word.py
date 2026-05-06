from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0009_stitchapplication_additional_comments_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompanyLead",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("company_name", models.CharField(max_length=180, verbose_name="Empresa")),
                ("contact_name", models.CharField(max_length=160, verbose_name="Nombre de contacto")),
                ("email", models.EmailField(max_length=254, verbose_name="Correo corporativo")),
                ("phone", models.CharField(max_length=30, verbose_name="Telefono / WhatsApp")),
                (
                    "company_size",
                    models.CharField(
                        choices=[
                            ("1_10", "1-10 colaboradores"),
                            ("11_50", "11-50 colaboradores"),
                            ("51_200", "51-200 colaboradores"),
                            ("200_mas", "200+ colaboradores"),
                        ],
                        max_length=20,
                        verbose_name="Tamano de empresa",
                    ),
                ),
                (
                    "service_interest",
                    models.CharField(
                        choices=[
                            ("ventas_seguros", "Venta de seguros de salud"),
                            ("atencion_cliente", "Atencion al cliente"),
                            ("soporte_comercial", "Soporte comercial"),
                            ("outsourcing", "Outsourcing de equipos"),
                            ("otro", "Otro"),
                        ],
                        max_length=40,
                        verbose_name="Servicio de interes",
                    ),
                ),
                ("message", models.TextField(blank=True, verbose_name="Necesidad o mensaje")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de contacto")),
            ],
            options={
                "verbose_name": "Contacto empresa",
                "verbose_name_plural": "Contactos empresas",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AlterField(
            model_name="application",
            name="cv",
            field=models.FileField(blank=True, null=True, upload_to="cvs/", verbose_name="Adjuntar CV (PDF o Word)"),
        ),
        migrations.AlterField(
            model_name="stitchapplication",
            name="cv",
            field=models.FileField(upload_to="cvs/", verbose_name="Adjuntar CV (PDF o Word)"),
        ),
    ]
