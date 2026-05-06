from django.urls import path

from .views import AboutView, CompanyLandingView, ContactView, HomeView, ServicesView

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("servicios/", ServicesView.as_view(), name="services"),
    path("quienes-somos/", AboutView.as_view(), name="about"),
    path("contacto/", ContactView.as_view(), name="contact"),
    path("empresas/", CompanyLandingView.as_view(), name="companies"),
]
