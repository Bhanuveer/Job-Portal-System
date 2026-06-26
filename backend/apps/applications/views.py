from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.permissions import IsRecruiter
from apps.common.responses import ApiResponse
from apps.jobs.services import JobService

from .models import Application
from .serializers import (
    ApplicationSerializer,
    MyApplicationSerializer,
    RecruiterApplicationSerializer,
)
from .services import ApplicationService


class ApplyJobView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):

        if request.user.role != "candidate":

            return ApiResponse.error(
                message="Only candidates can apply.",
                status=status.HTTP_403_FORBIDDEN,
            )

        job = JobService.get_job_by_id(job_id)

        serializer = ApplicationSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            application = (
                ApplicationService.apply_job(
                    request.user,
                    job,
                    serializer.validated_data,
                )
            )

        except ValueError as e:

            return ApiResponse.error(
                message=str(e),
                status=status.HTTP_400_BAD_REQUEST,
            )

        return ApiResponse.success(
            data=ApplicationSerializer(application).data,
            message="Application submitted successfully.",
            status=status.HTTP_201_CREATED,
        )


class JobApplicationsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRecruiter,
    ]

    def get(self, request, job_id):

        job = JobService.get_job_by_id(job_id)

        if job.recruiter != request.user:

            return ApiResponse.error(
                message="You can only view applications for your own jobs.",
                status=status.HTTP_403_FORBIDDEN,
            )

        applications = (
            ApplicationService
            .get_job_applications(job)
        )

        serializer = RecruiterApplicationSerializer(
            applications,
            many=True,
        )

        return ApiResponse.success(
            data=serializer.data,
            message="Applications fetched successfully.",
        )


class MyApplicationsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "candidate":

            return ApiResponse.error(
                message="Only candidates can access this endpoint.",
                status=status.HTTP_403_FORBIDDEN,
            )

        applications = (
            ApplicationService
            .get_candidate_applications(
                request.user
            )
        )

        serializer = MyApplicationSerializer(
            applications,
            many=True,
        )

        return ApiResponse.success(
            data=serializer.data,
            message="Applications fetched successfully.",
        )


class UpdateApplicationStatusView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRecruiter,
    ]

    def patch(self, request, application_id):

        application = (
            ApplicationService
            .get_application(application_id)
        )

        if application.job.recruiter != request.user:

            return ApiResponse.error(
                message="You cannot update applications for another recruiter's job.",
                status=status.HTTP_403_FORBIDDEN,
            )

        new_status = request.data.get("status")

        if new_status not in [
            Application.Status.PENDING,
            Application.Status.SHORTLISTED,
            Application.Status.REJECTED,
        ]:

            return ApiResponse.error(
                message="Invalid status.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        application = (
            ApplicationService.update_status(
                application,
                new_status,
            )
        )

        return ApiResponse.success(
            data={
                "status": application.status,
            },
            message="Application status updated successfully.",
        )