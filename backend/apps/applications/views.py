from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.jobs.services import JobService
from .serializers import ApplicationSerializer
from .services import ApplicationService
from .serializers import RecruiterApplicationSerializer, MyApplicationSerializer


class ApplyJobView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):

        if request.user.role != "candidate":

            return Response(
                {
                    "detail":
                    "Only candidates can apply."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        job = JobService.get_job_by_id(job_id)

        serializer = ApplicationSerializer(
            data=request.data
        )

        if serializer.is_valid():

            try:

                application = ApplicationService.apply_job(
                    request.user,
                    job,
                    serializer.validated_data
                )

                return Response(
                    ApplicationSerializer(application).data,
                    status=201
                )

            except ValueError as e:

                return Response(
                    {
                        "detail": str(e)
                    },
                    status=400
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class JobApplicationsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):

        if request.user.role != "recruiter":

            return Response(
                {
                    "detail": "Only recruiters can view applicants."
                },
                status=403
            )

        job = JobService.get_job_by_id(job_id)

        if job.recruiter != request.user:

            return Response(
                {
                    "detail": "Not your job."
                },
                status=403
            )

        applications = ApplicationService.get_job_applications(job)

        serializer = RecruiterApplicationSerializer(
            applications,
            many=True
        )

        return Response(serializer.data)
    
class MyApplicationsView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        if request.user.role != "candidate":

            return Response(
                {
                    "detail":
                    "Only candidates can access this."
                },
                status=403
            )

        applications = (
            ApplicationService
            .get_candidate_applications(
                request.user
            )
        )

        serializer = MyApplicationSerializer(
            applications,
            many=True
        )

        return Response(serializer.data)