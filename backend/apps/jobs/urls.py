from django.urls import path

from .views import (
    JobCreateView,
    JobDeleteView,
    JobDetailView,
    JobListView,
    JobUpdateView,
)

urlpatterns = [
    path(
        "",
        JobListView.as_view(),
        name="job-list",
    ),
    path(
        "create/",
        JobCreateView.as_view(),
        name="job-create",
    ),
    path(
        "<int:job_id>/",
        JobDetailView.as_view(),
        name="job-detail",
    ),
    path(
        "<int:job_id>/update/",
        JobUpdateView.as_view(),
        name="job-update",
    ),
    path(
        "<int:job_id>/delete/",
        JobDeleteView.as_view(),
        name="job-delete",
    ),
]