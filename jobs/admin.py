from django.contrib import admin

from .models import StitchApplication


@admin.register(StitchApplication)
class StitchApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone",
        "position",
        "sales_experience",
        "cv",
        "created_at",
    )
    list_filter = ("position", "sales_experience", "created_at")
    search_fields = ("full_name", "email", "phone")