from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username
    
import secrets


class APIKey(models.Model):
    class Scope(models.TextChoices):
        REPORTS = "reports", "Reports"
        TESTIMONIALS = "testimonials", "Testimonials"
        MATCHES = "matches", "Matches"
        ALL = "all", "Full access"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="api_keys")
    key = models.CharField(max_length=64, unique=True, editable=False)
    scope = models.CharField(max_length=20, choices=Scope.choices)
    label = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(32)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} — {self.get_scope_display()}"    