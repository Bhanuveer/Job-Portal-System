from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Job


class JobService:

    @staticmethod
    def create_job(validated_data, recruiter):

        validated_data["recruiter"] = recruiter

        return Job.objects.create(**validated_data)

    @staticmethod
    def get_active_jobs(
        search=None,
        location=None,
        experience_level=None,
        employment_type=None,
    ):

        jobs = (
            Job.objects
            .select_related("recruiter")
            .filter(is_active=True)
        )

        if search:
            jobs = jobs.filter(
                Q(title__icontains=search)
                | Q(company__icontains=search)
                | Q(skills__icontains=search)
            )

        if location:
            jobs = jobs.filter(
                location__iexact=location
            )

        if experience_level:
            jobs = jobs.filter(
                experience_level=experience_level
            )

        if employment_type:
            jobs = jobs.filter(
                employment_type=employment_type
            )

        return jobs

    @staticmethod
    def get_job_by_id(job_id):

        return get_object_or_404(
            Job,
            id=job_id,
            is_active=True,
        )

    @staticmethod
    def update_job(job, validated_data):

        for key, value in validated_data.items():
            setattr(job, key, value)

        job.save(
            update_fields=list(validated_data.keys())
        )

        return job

    @staticmethod
    def delete_job(job):

        job.delete()