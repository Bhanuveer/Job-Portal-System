from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.common.pagination import JobPagination
from .serializers import JobSerializer
from .permissions import IsRecruiter
from .services import JobService


class JobCreateView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRecruiter,
    ]

    def post(self, request):

        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():

            job = JobService.create_job(
                serializer.validated_data,
                request.user
            )

            response = JobSerializer(job)

            return Response(
                response.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
class JobListView(APIView):

    pagination = JobPagination()

    def get(self, request):

        search = request.query_params.get("search")
        location = request.query_params.get("location")
        experience_level = request.query_params.get("experience_level")
        employment_type = request.query_params.get("employment_type")

        jobs = JobService.get_active_jobs(
            search=search,
            location=location,
            experience_level=experience_level,
            employment_type=employment_type,
        )

        page = self.pagination.paginate_queryset(
            jobs,
            request
        )

        serializer = JobSerializer(
            page,
            many=True
        )

        return self.pagination.get_paginated_response(
            serializer.data
        )
    
    
class JobDetailView(APIView):

    def get(self, request, job_id):

        job = JobService.get_job_by_id(job_id)

        serializer = JobSerializer(job)

        return Response(serializer.data)
    

class JobUpdateView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRecruiter,
    ]

    def put(self, request, job_id):

        job = JobService.get_job_by_id(job_id)

        if job.recruiter != request.user:

            return Response(
                {
                    "detail":
                    "You can only update your own jobs."
                },
                status=403
            )

        serializer = JobSerializer(
            job,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            job = JobService.update_job(
                job,
                serializer.validated_data
            )

            return Response(
                JobSerializer(job).data
            )

        return Response(
            serializer.errors,
            status=400
        )
    
class JobDeleteView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRecruiter,
    ]

    def delete(self, request, job_id):

        job = JobService.get_job_by_id(job_id)

        if job.recruiter != request.user:

            return Response(
                {
                    "detail":
                    "You can only delete your own jobs."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        JobService.delete_job(job)

        return Response(
            {
                "message":
                "Job deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )