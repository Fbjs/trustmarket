from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from jobs.forms import StitchApplicationForm
from jobs.models import postulaciones
from jobs.views import notify_recruitment_team

class HomeView(FormView):
    template_name = "core/stitch_landing.html"
    form_class = StitchApplicationForm
    success_url = reverse_lazy("core:home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pasar los archivos subidos al formulario
        if self.request.method in ("POST", "PUT"):
            kwargs["files"] = self.request.FILES
        return kwargs

    def form_valid(self, form):
        application = form.save()
        
        # Guardamos en la tabla manual 'postulaciones'
        try:
            postulaciones.objects.create(
                nombre_completo=application.full_name,
                telefono=application.phone,
                email=application.email,
                edad=application.age,
                puesto=application.get_position_display(),
                experiencia_ventas=application.get_sales_experience_display(),
                disponibilidad=application.availability,
                cv_url=application.cv.url if application.cv else "",
                # StitchApplication no tiene comentarios adicionales?
                # Ah, sí los agregué al modelo y form.
                comentarios=application.additional_comments if hasattr(application, 'additional_comments') else ""
            )
        except Exception as e:
            print(f"Error guardando StitchApplication en tabla manual: {e}")

        notify_recruitment_team(application)
        messages.success(self.request, "¡Gracias por postular! Tu información fue recibida correctamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Mostrar errores específicos del formulario
        error_details = "; ".join(
            f"{field}: {', '.join(errs)}"
            for field, errs in form.errors.items()
            if field != "__all__"
        )
        mensaje = "Hubo un error en tu postulación."
        if error_details:
            mensaje += f" Revisa: {error_details}"
        else:
            mensaje += " Verifica que el CV sea un archivo PDF válido e intenta de nuevo."
        messages.error(self.request, mensaje)
        return super().form_invalid(form)

class ServicesView(TemplateView):
    template_name = "core/services.html"

class AboutView(TemplateView):
    template_name = "core/about.html"

class ContactView(TemplateView):
    template_name = "core/contact.html"
