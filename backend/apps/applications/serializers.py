from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:

        model = Application

        fields = "__all__"

        read_only_fields = (
            "candidate",
             "job",
            "status",
            "applied_at",
        )

class RecruiterApplicationSerializer(serializers.ModelSerializer):

    candidate_name = serializers.CharField(
        source="candidate.name",
        read_only=True
    )

    candidate_email = serializers.EmailField(
        source="candidate.email",
        read_only=True
    )

    class Meta:

        model = Application

        fields = [
            "id",
            "candidate_name",
            "candidate_email",
            "resume",
            "cover_letter",
            "status",
            "applied_at",
        ]

class MyApplicationSerializer(serializers.ModelSerializer):

    job_title = serializers.CharField(
        source="job.title",
        read_only=True
    )

    company = serializers.CharField(
        source="job.company",
        read_only=True
    )

    class Meta:

        model = Application

        fields = [
            "id",
            "job_title",
            "company",
            "status",
            "applied_at",
            "resume",
        ]