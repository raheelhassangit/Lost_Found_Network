from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Report, Category, Review
from .serializers import ReportSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly
from .matching import generate_matches_task


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.select_related("category", "user").all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["report_type", "status", "category"]
    search_fields = ["item_name", "description", "location"]
    ordering_fields = ["date", "created_at"]

    def perform_create(self, serializer):
        report = serializer.save(user=self.request.user)
        generate_matches_task.enqueue(report.pk)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        reports = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(reports)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def mark_processing(self, request, pk=None):
        report = self.get_object()
        if report.user != request.user:
            return Response({"detail": "Not your report."}, status=status.HTTP_403_FORBIDDEN)
        if report.status == Report.Status.OPEN:
            report.status = Report.Status.PROCESSING
            report.save(update_fields=["status"])
        return Response(self.get_serializer(report).data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def close(self, request, pk=None):
        report = self.get_object()
        if report.user != request.user:
            return Response({"detail": "Not your report."}, status=status.HTTP_403_FORBIDDEN)
        if report.status == Report.Status.CLOSED:
            return Response({"detail": "Already closed."}, status=status.HTTP_400_BAD_REQUEST)

        Review.objects.create(
            report=report, reviewed_by=request.user,
            comment=request.data.get("comment", ""),
        )
        report.status = Report.Status.CLOSED
        report.save(update_fields=["status"])
        return Response(self.get_serializer(report).data)