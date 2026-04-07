import threading
import requests
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from .models import postulaciones

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
                    puesto=application.get_job_position_display(),
                    experiencia_ventas=application.get_sales_experience_display(),
                    disponibilidad=application.availability,
                    comentarios=application.additional_comments
                )
            except Exception as e:
                print(f"Error guardando en la tabla manual postulaciones: {e}")

            _notify_team(application)
            threading.Thread(target=_send_whatsapp, args=(application.full_name, application.phone)).start()
            
            messages.success(
                request,
                "¡Gracias por postular! Tu información fue recibida correctamente.",
            )
            return redirect("jobs:apply")
        else:
            # Si el formulario no es válido, pasarlo al template
            messages.error(
                request,
                "Hubo un error en tu postulación. Por favor revisa los datos e intenta de nuevo.",
            )
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
            f"Puesto de interés: {application.get_job_position_display()}\n"
            f"Edad: {application.age}\n"
            f"Experiencia: {application.get_sales_experience_display()}\n"
            f"Disponibilidad: {application.availability}\n"
        ),
        from_email=None,
        recipient_list=["reclutamiento@trustmarket.cl"],
        fail_silently=True,
    )

def _send_whatsapp(name, phone):
    url = "https://call.neighbour.cl/api/whatsapp/enviar-template"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Limpiamos el número para que quede solo dígitos (e.g. de +56 9 -> 569)
    clean_phone = "".join(filter(str.isdigit, str(phone)))
    
    data = {
        "nombre_cuenta_meta": "TrustMarket",
        "nombre_template": "confirmacion_registro_trustmarket",
        "numero_whatsapp": clean_phone,
        "nombre_cliente": name
    }
    try:
        requests.post(url, json=data, headers=headers, timeout=10)
    except Exception as e:
        print(f"Error enviando mensaje de WhatsApp: {e}")