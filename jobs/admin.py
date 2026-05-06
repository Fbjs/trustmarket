from django.contrib import admin

from .models import CompanyLead, StitchApplication


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


@admin.register(CompanyLead)
class CompanyLeadAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "contact_name",
        "email",
        "phone",
        "service_interest",
        "created_at",
    )
    list_filter = ("service_interest", "company_size", "created_at")
    search_fields = ("company_name", "contact_name", "email", "phone")
