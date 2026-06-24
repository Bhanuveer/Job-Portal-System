from django.db import models

from apps.accounts.models import User
from apps.jobs.models import Job


class Application(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
    )

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    resume = models.FileField(
        upload_to="resumes/"
    )

    cover_letter = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            "candidate",
            "job",
        )

    def __str__(self):

        return f"{self.candidate.email} - {self.job.title}"