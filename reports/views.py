from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Report
from .forms import ReportForm


@login_required
def report_create_view(request, report_type):
    report_type = report_type.upper()
    if report_type not in Report.ReportType.values:
        raise Http404

    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.report_type = report_type
            report.save()
            messages.success(request, "Your report has been posted.")
            return redirect("core:home")
    else:
        form = ReportForm()

    return render(request, "reports/report_form.html", {
        "form": form,
        "report_type": report_type,
    })