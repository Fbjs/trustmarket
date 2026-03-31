from django.contrib import admin

<<<<<<< HEAD
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone",
        "email",
        "age",
        "sales_experience",
        "created_at",
    )
    list_filter = ("sales_experience", "created_at")
    search_fields = ("full_name", "phone", "email", "availability")
=======
# Register your models here.
>>>>>>> 2c7037a (Configuración inicial Django y MySQL)
