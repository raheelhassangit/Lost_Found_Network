from django import forms
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(5, "5"), (4, "4"), (3, "3"), (2, "2"), (1, "1")],
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Testimonial
        fields = ["rating", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell others about your experience..."}),
        }