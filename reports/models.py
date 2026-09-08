from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        

class Report(models.Model):
    class ReportType(models.TextChoices):
        LOST = "LOST", "Lost"
        FOUND = "FOUND", "Found"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        PROCESSING = "PROCESSING", "Processing"
        CLOSED = "CLOSED", "Closed"

    report_type = models.CharField(max_length=5, choices=ReportType.choices)
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    color = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=150)
    date = models.DateField(help_text="Date the item was lost/found")
    image = models.ImageField(upload_to="reports/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.report_type}] {self.item_name}"        