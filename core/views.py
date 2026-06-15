from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
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
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": True, "message": "Gracias. Recibimos los datos de tu empresa y te contactaremos pronto."})
        messages.success(self.request, "Gracias. Recibimos los datos de tu empresa y te contactaremos pronto.")
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors_dict = {field: [str(e) for e in errors] for field, errors in form.errors.items()}
            return JsonResponse({"success": False, "errors": errors_dict}, status=400)
        return super().form_invalid(form)


class PartnersView(TemplateView):
    template_name = "core/partners.html"
