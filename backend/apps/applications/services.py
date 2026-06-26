from django.shortcuts import get_object_or_404

from .models import Application


class ApplicationService:

    @staticmethod
    def apply_job(candidate, job, validated_data):

        if Application.objects.filter(
            candidate=candidate,
            job=job,
        ).exists():

            raise ValueError(
                "You have already applied for this job."
            )

        return Application.objects.create(
            candidate=candidate,
            job=job,
            resume=validated_data["resume"],
            cover_letter=validated_data.get(
                "cover_letter",
                "",
            ),
        )

    @staticmethod
    def get_job_applications(job):

        return (
            Application.objects
            .select_related(
                "candidate",
                "job",
            )
            .filter(job=job)
        )

    @staticmethod
    def get_candidate_applications(candidate):

        return (
            Application.objects
            .select_related("job")
            .filter(candidate=candidate)
        )

    @staticmethod
    def get_application(application_id):

        return get_object_or_404(
            Application.objects.select_related(
                "job",
                "candidate",
            ),
            id=application_id,
        )

    @staticmethod
    def update_status(application, status):

        application.status = status

        application.save(
            update_fields=["status"]
        )

        return application