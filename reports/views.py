from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Report
from .forms import ReportForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


@login_required
def report_update_view(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if report.user != request.user:
        raise PermissionDenied

    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, "Report updated.")
            return redirect("reports:detail", pk=report.pk)
    else:
        form = ReportForm(instance=report)

    return render(request, "reports/report_form.html", {
        "form": form,
        "report_type": report.report_type,
        "editing": True,
    })


@login_required
def report_delete_view(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if report.user != request.user:
        raise PermissionDenied

    if request.method == "POST":
        report.delete()
        messages.success(request, "Report deleted.")
        return redirect("core:home")

    return render(request, "reports/report_confirm_delete.html", {"report": report})

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
    
def report_detail_view(request, pk):
    report = get_object_or_404(Report.objects.select_related("category", "user"), pk=pk)
    return render(request, "reports/report_detail.html", {"report": report})    