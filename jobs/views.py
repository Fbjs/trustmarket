from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.http import FileResponse
from .models import Application, postulaciones

from .forms import ApplicationForm


def apply_view(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            
            # Guardamos explícitamente en la tabla manual 'postulaciones'
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
                    comentarios=application.additional_comments
                )
            except Exception as e:
                print(f"Error guardando en la tabla manual postulaciones: {e}")

            notify_recruitment_team(application)
            messages.success(
                request,
                "¡Gracias por postular! Tu información fue recibida correctamente.",
            )
            return redirect(request.POST.get("next") or reverse("jobs:apply"))
        else:
            # Si el formulario no es válido, redirigir a home con mensaje de error
            messages.error(
                request,
                "Hubo un error en tu postulación. Por favor revisa los datos e intenta de nuevo.",
            )
            return render(request, "jobs/apply.html", {"form": form})
    # GET requests a /jobs/ renderizan el formulario standalone
    form = ApplicationForm()
    return render(request, "jobs/apply.html", {"form": form})


def notify_recruitment_team(application):
    message_body = (
        "Se recibió una nueva postulación en TrustMarket.\n\n"
        f"Nombre: {application.full_name}\n"
        f"Teléfono: {application.phone}\n"
        f"Correo: {application.email}\n"
        f"Edad: {application.age}\n"
        f"Puesto: {application.get_position_display()}\n"
        f"Experiencia: {application.get_sales_experience_display()}\n"
        f"Disponibilidad: {application.availability}\n"
    )
    if application.cv:
        message_body += f"CV Adjunto: {application.cv.url}\n"

    send_mail(
        subject=f"Nueva postulación: [{application.get_position_display()}] {application.full_name}",
        message=message_body,
        from_email=None,
        recipient_list=["operaciones.trustmarket@gmail.com"],
        fail_silently=True,
    )


def download_cv(request, application_id):
    """
    Vista para descargar el CV de una postulación
    """
    application = get_object_or_404(Application, id=application_id)
    
    if application.cv:
        response = FileResponse(application.cv.open('rb'))
        response['Content-Disposition'] = f'attachment; filename="{application.full_name}_CV"'
        return response
    
    return redirect("jobs:apply")
