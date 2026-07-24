from pathlib import Path

from django import forms

from .models import Application, CompanyLead


ALLOWED_CV_EXTENSIONS = {".pdf", ".doc", ".docx"}
CV_ACCEPT_ATTR = ".pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def validate_cv_file(uploaded_file):
    extension = Path(uploaded_file.name).suffix.lower()
    if extension not in ALLOWED_CV_EXTENSIONS:
        raise forms.ValidationError("Sube tu CV en formato PDF o Word (.pdf, .doc, .docx).")
    return uploaded_file


class ApplicationForm(forms.ModelForm):
    AVAILABILITY_CHOICES = [
        ("fulltime", "FullTime"),
        ("freelancer", "Freelancer"),
    ]

    YES_NO_CHOICES = [
        ("Si", "Sí"),
        ("No", "No"),
    ]

    availability_options = forms.MultipleChoiceField(
        label="Disponibilidad",
        choices=AVAILABILITY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    equipamiento_audio = forms.ChoiceField(
        label="Cuento con auriculares de cintillo (headset) con micrófono integrado y conexión exclusiva por USB (No Bluetooth, no Jack 3.5mm)",
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )

    especificaciones_pc = forms.ChoiceField(
        label="Confirmo que mi propio equipo (PC/Laptop/Mac) cuenta con un mínimo de 8 GB de RAM, espacio en el disco disponible y sistema operativo actualizado (Windows 10/11 o macOS).",
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )

    conexion = forms.ChoiceField(
        label="Poseo conexión a internet por Wi-Fi o cable LAN",
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )

    competencias = forms.ChoiceField(
        label="Poseo un nivel de usuario suficiente para gestionar el PC de forma autónoma y resolver problemas básicos de configuración de audio o conectividad.",
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:
        model = Application
        fields = [
            "full_name",
            "phone",
            "email",
            "age",
            "position",
            "sales_experience",
            "equipamiento_audio",
            "especificaciones_pc",
            "conexion",
            "competencias",
            "cv",
            "additional_comments",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Tu nombre..."}),
            "phone": forms.TextInput(attrs={"type": "tel", "placeholder": "+56 9 1234 5678"}),
            "email": forms.EmailInput(attrs={"placeholder": "tu@email.com"}),
            "age": forms.NumberInput(attrs={"min": 18, "max": 70, "placeholder": "25"}),
            "position": forms.Select(attrs={"class": "field-select"}),
            "sales_experience": forms.Select(attrs={"class": "field-select"}),
            "cv": forms.FileInput(attrs={"accept": CV_ACCEPT_ATTR, "id": "cv-upload"}),
            "additional_comments": forms.Textarea(attrs={"rows": 4, "placeholder": "Dinos algo más sobre ti..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "position" in self.fields:
            self.fields["position"].initial = "ejecutivo_ventas"
            if hasattr(self.fields["position"], "choices"):
                self.fields["position"].choices = [
                    (k, v) for k, v in self.fields["position"].choices if k != "ejecutivo_encuestas"
                ]
        for name, field in self.fields.items():
            field.required = True if name != "additional_comments" else False
            if name not in ["availability_options", "equipamiento_audio", "especificaciones_pc", "conexion", "competencias"]:
                existing = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = f"field-input {existing}".strip()

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "")
        import re
        cleaned = re.sub(r"[\s\-\(\)\.]", "", phone)
        phone_regex = re.compile(r"^(\+?56)?([2-9]\d{8})$")
        if not phone_regex.match(cleaned):
            raise forms.ValidationError(
                "El número de teléfono no es válido para Chile. Debe tener 9 dígitos (ej: 9 1234 5678 o +56 9 1234 5678)."
            )
        return phone

    def clean_age(self):
        age = self.cleaned_data["age"]
        if age < 18:
            raise forms.ValidationError("La edad mínima para postular es 18 años.")
        return age

    def clean_availability_options(self):
        values = self.cleaned_data.get("availability_options", [])
        if not values:
            raise forms.ValidationError("Selecciona al menos una franja horaria.")
        return values

    def clean_cv(self):
        cv = self.cleaned_data.get("cv")
        if cv:
            validate_cv_file(cv)
        return cv

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected = self.cleaned_data.get("availability_options", [])
        # Handle dict choices lookup
        choices_dict = dict(self.AVAILABILITY_CHOICES)
        instance.availability = ", ".join(choices_dict[v] for v in selected if v in choices_dict)
        if commit:
            instance.save()
        return instance




class CompanyLeadForm(forms.ModelForm):
    class Meta:
        model = CompanyLead
        fields = [
            "company_name",
            "contact_name",
            "email",
            "phone",
            "company_size",
            "service_interest",
            "message",
        ]
        widgets = {
            "company_name": forms.TextInput(attrs={"placeholder": "Nombre de la empresa"}),
            "contact_name": forms.TextInput(attrs={"placeholder": "Nombre y apellido"}),
            "email": forms.EmailInput(attrs={"placeholder": "contacto@empresa.com"}),
            "phone": forms.TextInput(attrs={"type": "tel", "placeholder": "+56 9 1234 5678"}),
            "company_size": forms.Select(),
            "service_interest": forms.Select(),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "Cuentanos que necesitas resolver o mejorar"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.required = name != "message"
            field.widget.attrs["class"] = (
                "w-full bg-white/10 border border-white/10 rounded-xl px-4 py-3 text-white "
                "placeholder:text-white/40 focus:border-primary-container focus:ring-2 "
                "focus:ring-primary-container/20 outline-none transition-all"
            )
