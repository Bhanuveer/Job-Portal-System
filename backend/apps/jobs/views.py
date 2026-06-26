from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.pagination import JobPagination
from apps.common.permissions import (
    IsJobOwner,
    IsRecruiter,
)
from apps.common.responses import ApiResponse

from .serializers import JobSerializer
from .services import JobService

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)


@extend_schema(
    tags=["Jobs"],
    summary="Create Job",
    description=(
        "Create a new job posting. "
        "Only authenticated recruiters can create jobs."
    ),
    request=JobSerializer,
    responses={
        201: JobSerializer,
        400: OpenApiResponse(
            description="Validation Error",
        ),
        401: OpenApiResponse(
            description="Authentication required",
        ),
        403: OpenApiResponse(
            description="Only recruiters can create jobs",
        ),
    },
    examples=[
        OpenApiExample(
            "Create Job",
            value={
                "title": "Python Backend Developer",
                "company": "Google",
                "location": "Bangalore",
                "description": "Build scalable backend APIs.",
                "skills": "Python, Django, DRF",
                "salary": 1200000,
                "employment_type": "full_time",
                "experience_level": "junior",
                "is_active": True,
            },
            request_only=True,
        )
    ],
)
class JobCreateView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRecruiter,
    ]

    serializer_class = JobSerializer

    def post(self, request):

        serializer = JobSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        job = JobService.create_job(
            serializer.validated_data,
            request.user,
        )

        return ApiResponse.success(
            data=JobSerializer(job).data,
            message="Job created successfully.",
            status_code=status.HTTP_201_CREATED,
        )


class JobListView(APIView):

    pagination = JobPagination()

    def get(self, request):

        jobs = JobService.get_active_jobs(
            search=request.query_params.get("search"),
            location=request.query_params.get("location"),
            experience_level=request.query_params.get(
                "experience_level"
            ),
            employment_type=request.query_params.get(
                "employment_type"
            ),
        )

        page = self.pagination.paginate_queryset(
            jobs,
            request,
        )

        serializer = JobSerializer(
            page,
            many=True,
        )

        return self.pagination.get_paginated_response(
            serializer.data
        )


class JobDetailView(APIView):

    def get(self, request, job_id):

        job = JobService.get_job_by_id(job_id)

        serializer = JobSerializer(job)

        return ApiResponse.success(
            data=serializer.data,
            message="Job fetched successfully.",
        )


class JobUpdateView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRecruiter,
        IsJobOwner,
    ]

    def put(self, request, job_id):

        job = JobService.get_job_by_id(job_id)

        self.check_object_permissions(
            request,
            job,
        )

        serializer = JobSerializer(
            job,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        job = JobService.update_job(
            job,
            serializer.validated_data,
        )

        return ApiResponse.success(
            data=JobSerializer(job).data,
            message="Job updated successfully.",
        )


class JobDeleteView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRecruiter,
        IsJobOwner,
    ]

    def delete(self, request, job_id):

        job = JobService.get_job_by_id(job_id)

        self.check_object_permissions(
            request,
            job,
        )

        JobService.delete_job(job)

        return ApiResponse.success(
            message="Job deleted successfully.",
        )