<<<<<<< HEAD
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "core/home.html"


class ServicesView(TemplateView):
    template_name = "core/services.html"


class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactView(TemplateView):
    template_name = "core/contact.html"
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> 2c7037a (Configuración inicial Django y MySQL)
