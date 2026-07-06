from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.http import FileResponse, JsonResponse
from .models import Application, postulaciones

from .forms import ApplicationForm


from django.views.decorators.cache import never_cache


@never_cache
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
                    comentarios=application.additional_comments,
                    equipamiento_audio=application.equipamiento_audio,
                    especificaciones_pc=application.especificaciones_pc,
                    conexion=application.conexion,
                    competencias=application.competencias,
                )
            except Exception as e:
                print(f"Error guardando en la tabla manual postulaciones: {e}")

            notify_recruitment_team(application)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": True})
            messages.success(
                request,
                "¡Gracias por postular! Tu información fue recibida correctamente.",
            )
            return redirect(request.POST.get("next") or reverse("jobs:apply"))
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                errors_dict = {field: [str(error) for error in errors] for field, errors in form.errors.items()}
                return JsonResponse({"success": False, "errors": errors_dict}, status=400)
            
            # Serialize form data to standard types for session storage
            form_data_dict = {k: request.POST.getlist(k) for k in request.POST}
            errors_dict = {field: [str(error) for error in errors] for field, errors in form.errors.items()}
            
            request.session['apply_form_data'] = form_data_dict
            request.session['apply_form_errors'] = errors_dict
            
            messages.error(request, "Hay un error en los campos. Por favor revisa y corrige los campos marcados en rojo.")
            
            # Enforce GET redirect to prevent form resubmission prompts (PRG pattern)
            redirect_url = reverse("jobs:apply")
            query_string = request.META.get('QUERY_STRING', '')
            if query_string:
                redirect_url += f"?{query_string}"
            return redirect(redirect_url)
            
    # GET requests a /jobs/ renderizan el formulario standalone
    form_data = request.session.pop('apply_form_data', None)
    form_errors = request.session.pop('apply_form_errors', None)
    
    if form_data:
        from django.http import QueryDict
        # Reconstruct QueryDict to preserve multi-value lists correctly in form cleaning
        qd = QueryDict(mutable=True)
        for k, v in form_data.items():
            qd.setlist(k, v)
        form = ApplicationForm(qd)
        if form_errors:
            for field, errors in form_errors.items():
                for error in errors:
                    form.add_error(field, error)
    else:
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
        import os
        ext = os.path.splitext(application.cv.name)[1]
        filename = f"{application.full_name}_CV{ext}"
        return FileResponse(
            application.cv.open('rb'),
            as_attachment=True,
            filename=filename
        )
    
    return redirect("jobs:apply")
