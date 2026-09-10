from django import forms
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(choices=[(i, i) for i in range(1, 6)]),
            "comment": forms.Textarea(attrs={"rows": 3}),
        }