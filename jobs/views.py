<<<<<<< HEAD
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from .models import postulaciones

from .forms import ApplicationForm


def apply_view(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            _notify_team(application)
            messages.success(
                request,
                "¡Gracias por postular! Tu información fue recibida correctamente.",
            )
            return redirect("jobs:apply")
    else:
        form = ApplicationForm()

    return render(request, "jobs/apply.html", {"form": form})


def _notify_team(application):
    send_mail(
        subject=f"Nueva postulación: {application.full_name}",
        message=(
            "Se recibió una nueva postulación en TrustMarket.\n\n"
            f"Nombre: {application.full_name}\n"
            f"Teléfono: {application.phone}\n"
            f"Correo: {application.email}\n"
            f"Edad: {application.age}\n"
            f"Experiencia: {application.get_sales_experience_display()}\n"
            f"Disponibilidad: {application.availability}\n"
        ),
        from_email=None,
        recipient_list=["reclutamiento@trustmarket.cl"],
        fail_silently=True,
    )


def enviar_postulacion(request):
    if request.method == 'POST':
        # Captura de checkboxes (getlist es vital para varios valores)
        disponibilidad_lista = request.POST.getlist('disponibilidad[]')
        disponibilidad_str = ", ".join(disponibilidad_lista)

        # Crear registro en la tabla manual
        Postulaciones.objects.create(
            nombre_completo=request.POST.get('nombre'),
            telefono=request.POST.get('telefono'),
            email=request.POST.get('email'),
            edad=request.POST.get('edad'),
            experiencia_ventas=request.POST.get('experiencia'),
            disponibilidad=disponibilidad_str,
            comentarios=request.POST.get('comentarios')
        )
        return render(request, 'exito.html')
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> 2c7037a (Configuración inicial Django y MySQL)
