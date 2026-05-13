from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView 
from .sitemaps import StaticViewSitemap
from .views import robots_txt

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("", include("core.urls")),
    path("jobs/", include("jobs.urls")),
    
    # Ruta para la verificación de Google Search Console
    path(
        "google193bb166c2f3320a.html", 
        TemplateView.as_view(template_name="google193bb166c2f3320a.html", content_type="text/html")
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
