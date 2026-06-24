from .models import Job
from django.shortcuts import get_object_or_404

class JobService:

    @staticmethod
    def create_job(validated_data, recruiter):

        validated_data["recruiter"] = recruiter

        return Job.objects.create(**validated_data)
    
    
    @staticmethod
    def get_active_jobs():

        return (
            Job.objects
            .filter(is_active=True)
            .order_by("-created_at")
        )
    
    @staticmethod
    def get_job_by_id(job_id):

        return get_object_or_404(
            Job,
            id=job_id,
            is_active=True
        )