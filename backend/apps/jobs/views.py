from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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

    def get(self, request):

        jobs = JobService.get_active_jobs()

        serializer = JobSerializer(
            jobs,
            many=True
        )

        return Response(serializer.data)
    
class JobDetailView(APIView):

    def get(self, request, job_id):

        job = JobService.get_job_by_id(job_id)

        serializer = JobSerializer(job)

        return Response(serializer.data)