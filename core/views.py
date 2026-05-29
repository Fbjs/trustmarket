from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from jobs.forms import CompanyLeadForm

class HomeView(TemplateView):
    template_name = "core/stitch_landing.html"

class ServicesView(TemplateView):
    template_name = "core/services.html"

class AboutView(TemplateView):
    template_name = "core/about.html"

class ContactView(TemplateView):
    template_name = "core/contact.html"


class CompanyLandingView(FormView):
    template_name = "core/company_landing.html"
    form_class = CompanyLeadForm
    success_url = reverse_lazy("core:companies")

    def form_valid(self, form):
        lead = form.save()
        send_mail(
            subject=f"Nuevo contacto empresa: {lead.company_name}",
            message=(
                "Se recibio una nueva solicitud de empresa en TrustMarket.\n\n"
                f"Empresa: {lead.company_name}\n"
                f"Contacto: {lead.contact_name}\n"
                f"Correo: {lead.email}\n"
                f"Telefono: {lead.phone}\n"
                f"Tamano: {lead.get_company_size_display()}\n"
                f"Servicio: {lead.get_service_interest_display()}\n"
                f"Mensaje: {lead.message}\n"
            ),
            from_email=None,
            recipient_list=["operaciones.trustmarket@gmail.com"],
            fail_silently=True,
        )
        messages.success(self.request, "Gracias. Recibimos los datos de tu empresa y te contactaremos pronto.")
        return super().form_valid(form)


class PartnersView(TemplateView):
    template_name = "core/partners.html"
