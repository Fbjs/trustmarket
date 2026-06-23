from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
from datetime import datetime

from .models import Application, CompanyLead


def export_to_excel(modeladmin, request, queryset):
    """
    Acción personalizada para exportar registros a Excel con hipervínculos a CVs
    """
    # Crear un nuevo libro de Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Registros"
    
    # Obtener los nombres de los campos a exportar
    fields = [field.name for field in modeladmin.model._meta.fields]
    
    # Crear encabezados con estilo
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    
    for col_num, field_name in enumerate(fields, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = field_name.upper()
        cell.fill = header_fill
        cell.font = header_font
    
    # Agregar datos
    for row_num, obj in enumerate(queryset, 2):
        for col_num, field_name in enumerate(fields, 1):
            cell = ws.cell(row=row_num, column=col_num)
            value = getattr(obj, field_name)
            
            # Si el campo es un archivo CV y el objeto tiene ID, crear hipervínculo
            if field_name == 'cv' and value and hasattr(obj, 'id'):
                cv_url = request.build_absolute_uri(
                    reverse('jobs:download_cv', args=[obj.id])
                )
                cell.value = f"Descargar CV"
                cell.hyperlink = cv_url
                cell.font = Font(color="0563C1", underline="single")
            else:
                cell.value = str(value) if value else ""
    
    # Ajustar ancho de columnas
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Crear respuesta HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename=registros_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    wb.save(response)
    return response


export_to_excel.short_description = "Descargar registros en Excel"





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
    actions = [export_to_excel]

    class Media:
        css = {
            "all": ("css/admin_custom.css",)
        }


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone",
        "position",
        "sales_experience",
        "availability",
        "equipamiento_audio",
        "especificaciones_pc",
        "conexion",
        "competencias",
        "cv",
        "created_at",
    )
    list_filter = (
        "position",
        "sales_experience",
        "availability",
        "equipamiento_audio",
        "especificaciones_pc",
        "conexion",
        "competencias",
        "created_at",
    )
    search_fields = ("full_name", "email", "phone")
    actions = [export_to_excel]

    class Media:
        css = {
            "all": ("css/admin_custom.css",)
        }

