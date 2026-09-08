from django.contrib import admin
from .models import Category, Report


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["item_name", "report_type", "status", "category", "user", "date"]
    list_filter = ["report_type", "status", "category"]
    search_fields = ["item_name", "description", "location"]