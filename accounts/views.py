from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import SignUpForm


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("reports:list")  # we'll build this view next
        return render(request, "accounts/signup.html", {"form": form})

    form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})