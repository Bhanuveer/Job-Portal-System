from .models import Application


class ApplicationService:

    @staticmethod
    def apply_job(candidate, job, data):

        if Application.objects.filter(
            candidate=candidate,
            job=job
        ).exists():

            raise ValueError(
                "You have already applied for this job."
            )

        return Application.objects.create(
            candidate=candidate,
            job=job,
            resume=data["resume"],
            cover_letter=data.get("cover_letter", "")
        )

    @staticmethod
    def get_job_applications(job):

        return Application.objects.filter(job=job)
    
    @staticmethod
    def get_candidate_applications(candidate):

        return Application.objects.filter(
            candidate=candidate
        ).order_by("-applied_at")