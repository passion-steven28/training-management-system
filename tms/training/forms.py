from django import forms
from .models import Session, Evaluation, PreAssessment, PostAssessment


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = [
            "course",
            "title",
            "date",
            "duration",
            "venue",
            "is_online",
            "meeting_link",
            "trainer",
        ]
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ["content_rating", "trainer_rating", "feedback"]
        widgets = {
            "feedback": forms.Textarea(attrs={"rows": 4}),
        }


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = PreAssessment
        fields = ["score"]
