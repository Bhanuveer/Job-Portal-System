from django.urls import path

from .views import (
    ApplyJobView,
    JobApplicationsView,
    MyApplicationsView,
    UpdateApplicationStatusView,
)

urlpatterns = [
    path(
        "jobs/<int:job_id>/apply/",
        ApplyJobView.as_view(),
        name="apply-job",
    ),
    path(
        "jobs/<int:job_id>/applications/",
        JobApplicationsView.as_view(),
        name="job-applications",
    ),
    path(
        "applications/my/",
        MyApplicationsView.as_view(),
        name="my-applications",
    ),
    path(
        "applications/<int:application_id>/status/",
        UpdateApplicationStatusView.as_view(),
        name="application-status",
    ),
]