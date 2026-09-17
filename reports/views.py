from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .models import Report, Category, Match, Review
from .forms import ReportForm, ReviewForm
from .matching import generate_matches


def report_list_view(request):
    reports = Report.objects.select_related("category", "user").order_by("-created_at")

    report_type = request.GET.get("type")
    if report_type in Report.ReportType.values:
        reports = reports.filter(report_type=report_type)

    status = request.GET.get("status")
    if status in Report.Status.values:
        reports = reports.filter(status=status)

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
        "selected_status": status or "",
        "selected_category": category_id or "",
        "query": query or "",
        "querystring": params.urlencode(),
    })


@login_required
def my_reports_view(request):
    reports = Report.objects.filter(user=request.user).select_related("category").order_by("-created_at")
    matched_report_ids = set(
        Match.objects.filter(primary_report__user=request.user).values_list("primary_report_id", flat=True)
    )
    return render(request, "reports/my_reports.html", {
        "reports": reports,
        "matched_report_ids": matched_report_ids,
    })


@login_required
def my_matches_view(request):
    matches = Match.objects.filter(
        primary_report__user=request.user
    ).select_related("primary_report", "matched_report", "matched_report__user").order_by("-score")
    return render(request, "reports/my_matches.html", {"matches": matches})


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
            generate_matches(report)
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
def report_close_view(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if report.user != request.user:
        raise PermissionDenied
    if report.status == Report.Status.CLOSED:
        return redirect("reports:detail", pk=report.pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.report = report
            review.reviewed_by = request.user
            review.save()
            report.status = Report.Status.CLOSED
            report.save(update_fields=["status"])
            messages.success(request, "Report marked as resolved.")
            return redirect("reports:my_reports")
    else:
        form = ReviewForm()

    return render(request, "reports/report_close.html", {"form": form, "report": report})

@login_required
def confirm_match_view(request, match_id):
    if request.method != "POST":
        return redirect("reports:my_matches")
    match = get_object_or_404(Match, pk=match_id)
    if match.primary_report.user != request.user:
        raise PermissionDenied

    match.confirmed = True
    match.save(update_fields=["confirmed"])

    mirror = Match.objects.filter(
        primary_report=match.matched_report,
        matched_report=match.primary_report,
    ).first()

    if mirror and mirror.confirmed:
        for report in [match.primary_report, match.matched_report]:
            if not hasattr(report, "review"):
                Review.objects.create(report=report, reviewed_by=report.user, comment="Resolved via match confirmation.")
            report.status = Report.Status.CLOSED
            report.save(update_fields=["status"])
        messages.success(request, "Both sides confirmed — marked resolved!")
    else:
        messages.success(request, "Confirmed. Waiting for the other side to confirm too.")

    return redirect("reports:my_matches")

@login_required
def report_mark_processing_view(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if report.user != request.user:
        raise PermissionDenied

    if request.method == "POST" and report.status == Report.Status.OPEN:
        report.status = Report.Status.PROCESSING
        report.save(update_fields=["status"])
        messages.success(request, "Marked as in progress.")

    return redirect("reports:my_reports")