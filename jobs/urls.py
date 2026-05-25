from django.urls import path

from .views import apply_view, download_cv

app_name = "jobs"

urlpatterns = [
    path("", apply_view, name="apply"),
    path("download-cv/<int:application_id>/", download_cv, name="download_cv"),
]
