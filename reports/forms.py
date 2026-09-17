from django import forms
from .models import Report, Review


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["category", "item_name", "description", "color", "location", "date", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "date": forms.DateInput(attrs={"type": "date"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "How did it get resolved?"}),
        }