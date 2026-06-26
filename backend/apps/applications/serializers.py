from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:

        model = Application

        fields = [
            "id",
            "candidate",
            "job",
            "resume",
            "cover_letter",
            "status",
            "applied_at",
        ]

        read_only_fields = [
            "id",
            "candidate",
            "job",
            "status",
            "applied_at",
        ]

    def validate_resume(self, value):

        if value.size > 5 * 1024 * 1024:

            raise serializers.ValidationError(
                "Resume size must be less than 5 MB."
            )

        return value


class RecruiterApplicationSerializer(serializers.ModelSerializer):

    candidate_name = serializers.CharField(
        source="candidate.name",
        read_only=True,
    )

    candidate_email = serializers.EmailField(
        source="candidate.email",
        read_only=True,
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

        read_only_fields = fields


class MyApplicationSerializer(serializers.ModelSerializer):

    job_title = serializers.CharField(
        source="job.title",
        read_only=True,
    )

    company = serializers.CharField(
        source="job.company",
        read_only=True,
    )

    class Meta:

        model = Application

        fields = [
            "id",
            "job_title",
            "company",
            "resume",
            "status",
            "applied_at",
        ]

        read_only_fields = fields