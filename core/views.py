from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from reports.models import Report
from .models import Testimonial
from .forms import TestimonialForm


def home_view(request):
    recent_reports = Report.objects.select_related("category", "user").order_by("-created_at")[:6]
    testimonials = Testimonial.objects.select_related("user")[:6]
    return render(request, "core/home.html", {
        "recent_reports": recent_reports,
        "testimonials": testimonials,
    })


@login_required
def add_testimonial_view(request):
    if request.method == "POST":
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            messages.success(request, "Thanks for your feedback!")
            return redirect("core:home")
    else:
        form = TestimonialForm()

    return render(request, "core/add_testimonial.html", {"form": form})