from django.contrib import admin
from .models import Category, Report, Match, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["item_name", "report_type", "status", "category", "user", "date"]
    list_filter = ["report_type", "status", "category"]
    search_fields = ["item_name", "description", "location"]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ["primary_report", "matched_report", "score", "created_at"]
    list_filter = ["score"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["report", "reviewed_by", "created_at"]