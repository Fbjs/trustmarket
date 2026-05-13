from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("jobs/", include("jobs.urls")),
    
    # Ruta para la verificación de Google Search Console
    path(
        "google193bb166c2f3320a.html", 
        TemplateView.as_view(template_name="google193bb166c2f3320a.html", content_type="text/html")
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)