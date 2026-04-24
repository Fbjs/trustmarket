from django import forms

from .models import Application


class ApplicationForm(forms.ModelForm):
    AVAILABILITY_CHOICES = [
        ("manana", "Mañana"),
        ("tarde", "Tarde"),
        ("noche", "Noche"),
        ("fines_semana", "Fines de semana"),
    ]

    availability_options = forms.MultipleChoiceField(
        label="Disponibilidad",
        choices=AVAILABILITY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
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
            "cv",
            "additional_comments",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Tu nombre..."}),
            "phone": forms.TextInput(attrs={"placeholder": "+56 9..."}),
            "email": forms.EmailInput(attrs={"placeholder": "tu@email.com"}),
            "age": forms.NumberInput(attrs={"min": 18, "max": 70, "placeholder": "25"}),
            "position": forms.Select(attrs={"class": "field-select"}),
            "sales_experience": forms.Select(attrs={"class": "field-select"}),
            "cv": forms.FileInput(attrs={"accept": ".pdf", "id": "cv-upload"}),
            "additional_comments": forms.Textarea(attrs={"rows": 4, "placeholder": "Dinos algo más sobre ti..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.required = True if name != "additional_comments" else False
            if name != "availability_options":
                existing = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = f"field-input {existing}".strip()

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

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected = self.cleaned_data.get("availability_options", [])
        # Handle dict choices lookup
        choices_dict = dict(self.AVAILABILITY_CHOICES)
        instance.availability = ", ".join(choices_dict[v] for v in selected if v in choices_dict)
        if commit:
            instance.save()
        return instance

from .models import StitchApplication

class StitchApplicationForm(forms.ModelForm):
    AVAILABILITY_CHOICES = [
        ("manana", "Mañana"),
        ("tarde", "Tarde"),
        ("noche", "Noche"),
        ("fines_semana", "Fines de semana"),
    ]

    availability_options = forms.MultipleChoiceField(
        label="Disponibilidad",
        choices=AVAILABILITY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = StitchApplication
        fields = [
            "full_name",
            "email",
            "phone",
            "age",
            "position",
            "sales_experience",
            "cv",
            "additional_comments",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Ej. Juan Pérez", "class": "w-full bg-surface-container-high border-none rounded-lg p-4 focus:ring-2 focus:ring-primary-container outline-none transition-all"}),
            "email": forms.EmailInput(attrs={"placeholder": "juan@email.com", "class": "w-full bg-surface-container-high border-none rounded-lg p-4 focus:ring-2 focus:ring-primary-container outline-none transition-all"}),
            "phone": forms.TextInput(attrs={"placeholder": "+56 9 1234 5678", "class": "w-full bg-surface-container-high border-none rounded-lg p-4 focus:ring-2 focus:ring-primary-container outline-none transition-all"}),
            "age": forms.NumberInput(attrs={"placeholder": "25", "class": "w-full bg-surface-container-high border-none rounded-lg p-4 focus:ring-2 focus:ring-primary-container outline-none transition-all"}),
            "position": forms.Select(attrs={"class": "w-full bg-surface-container-high border-none rounded-lg p-4 focus:ring-2 focus:ring-primary-container outline-none transition-all"}),
            "sales_experience": forms.Select(attrs={"class": "w-full bg-surface-container-high border-none rounded-lg p-4 focus:ring-2 focus:ring-primary-container outline-none transition-all"}),
            "cv": forms.FileInput(attrs={"id": "cv-upload", "class": "hidden", "accept": ".pdf"}),
            "additional_comments": forms.Textarea(attrs={"rows": 4, "placeholder": "Dinos algo más sobre ti...", "class": "w-full bg-surface-container-high border-none rounded-lg p-4 focus:ring-2 focus:ring-primary-container outline-none transition-all"}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected = self.cleaned_data.get("availability_options", [])
        choices_dict = dict(self.AVAILABILITY_CHOICES)
        instance.availability = ", ".join(choices_dict[v] for v in selected if v in choices_dict)
        if commit:
            instance.save()
        return instance
