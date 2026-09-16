from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Report, Category
from .forms import ReportForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q



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

def report_list_view(request):
    reports = Report.objects.select_related("category", "user").order_by("-created_at")

    report_type = request.GET.get("type")
    if report_type in Report.ReportType.values:
        reports = reports.filter(report_type=report_type)

    category_id = request.GET.get("category")
    if category_id:
        reports = reports.filter(category_id=category_id)

    query = request.GET.get("q")
    if query:
        reports = reports.filter(
            Q(item_name__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

    paginator = Paginator(reports, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    params = request.GET.copy()
    params.pop("page", None)

    return render(request, "reports/report_list.html", {
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "selected_type": report_type or "",
        "selected_category": category_id or "",
        "query": query or "",
        "querystring": params.urlencode(),
    })
    
@login_required
def my_reports_view(request):
    reports = Report.objects.filter(user=request.user).select_related("category").order_by("-created_at")
    return render(request, "reports/my_reports.html", {"reports": reports})    