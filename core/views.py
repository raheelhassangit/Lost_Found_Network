from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.models import APIKey
from reports.models import Report
from .models import Testimonial
from .forms import TestimonialForm
from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken

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


def support_view(request):
    return render(request, "core/support.html", {
        "support_email": settings.PLATFORM_SUPPORT_EMAIL,
    })

@login_required
def get_api_view(request):
    new_key_value = None

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "generate":
            new_key = APIKey.objects.create(
                user=request.user,
                scope=request.POST.get("scope"),
                label=request.POST.get("label", ""),
            )
            new_key_value = new_key.key
        elif action == "revoke":
            APIKey.objects.filter(pk=request.POST.get("key_id"), user=request.user).update(is_active=False)
            return redirect("core:get_api")

        refresh = RefreshToken.for_user(request.user)
        return render(request, "core/get_api.html", {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "api_keys": request.user.api_keys.filter(is_active=True),
            "scopes": APIKey.Scope.choices,
            "new_key_value": new_key_value,
        })

    refresh = RefreshToken.for_user(request.user)
    return render(request, "core/get_api.html", {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "api_keys": request.user.api_keys.filter(is_active=True),
        "scopes": APIKey.Scope.choices,
        "new_key_value": None,
    })
    
def terms_view(request):
    return render(request, "core/terms.html")

def privacy_view(request):
    return render(request, "core/privacy.html")    