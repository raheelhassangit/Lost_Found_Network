from rest_framework import serializers
from .models import Report, Category, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ReportSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = Report
        fields = [
            "id", "report_type", "item_name", "description", "category", "category_name",
            "color", "location", "date", "image", "status", "user", "created_at", "updated_at",
        ]
        read_only_fields = ["status", "user"]
        
class ReviewSerializer(serializers.ModelSerializer):
    reviewed_by = serializers.ReadOnlyField(source="reviewed_by.username")

    class Meta:
        model = Review
        fields = ["id", "report", "reviewed_by", "comment", "created_at"]
        read_only_fields = ["report", "reviewed_by"]        