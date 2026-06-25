from django.urls import path

from .views import ApplyJobView, JobApplicationsView, MyApplicationsView

urlpatterns = [

    path(
        "jobs/<int:job_id>/apply/",
        ApplyJobView.as_view(),
        name="apply-job",
    ),

    path(
        "jobs/<int:job_id>/applications/",
        JobApplicationsView.as_view()
    ),

    path(
        "applications/my/",
        MyApplicationsView.as_view(),
        name="my-applications",
    ),

]