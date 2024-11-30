from django import forms
from .models import Course, Material, Category


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "title",
            "cover_image",
            "category",
            "description",
            "start_date",
            "end_date",
            "capacity",
            "is_online",
            "trainers",
        ]
        widgets = {
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["title", "description", "file"]
