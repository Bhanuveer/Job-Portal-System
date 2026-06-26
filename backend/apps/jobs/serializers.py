from rest_framework import serializers

from .models import Job


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job

        fields = [
            "id",
            "recruiter",
            "title",
            "company",
            "location",
            "description",
            "skills",
            "salary",
            "employment_type",
            "experience_level",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "recruiter",
            "created_at",
            "updated_at",
        ]

    def validate_salary(self, value):

        if value < 1000:
            raise serializers.ValidationError(
                "Salary must be at least 1000."
            )

        return value