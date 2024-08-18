from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from surveysv.surveys.models import Survey, SurveyVersion

from .details import SurveyDetailsSerializer


class SurveyListSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField()

    class Meta:
        model = Survey
        fields = ["id", "title", "created", "updated", "question_count"]


class SurveyCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = ["id", "title"]

    def create(self, validated_data):
        survey = Survey.objects.create(**validated_data)
        return survey


class SurveyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ["id", "title"]

    def update(self, instance, validated_data):

        # Update the survey fields
        instance.title = validated_data.get("title", instance.title)
        instance.save()

        return instance


class SurveyVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyVersion
        fields = ["survey", "created", "version_name", "version_code", "body"]


class SurveyGenerateVersionSerializer(serializers.Serializer):
    version_name = serializers.CharField(max_length=25)
    version_code = serializers.SlugField(max_length=25)

    def validate(self, data):
        version_code = data["version_code"]
        survey_pk = self.context["survey_pk"]

        # Check if the survey exists
        try:
            survey = Survey.objects.get(pk=survey_pk)
        except Survey.DoesNotExist:
            raise NotFound(f"Survey with id {survey_pk} not found.")

        # Check if a version with this code already exists for the survey
        if SurveyVersion.objects.filter(
            survey_id=survey_pk, version_code=version_code
        ).exists():
            raise ValidationError(
                {
                    "version_code": f"A version with code '{version_code}' already exists for this survey."
                }
            )

        # Add the survey to the validated data
        data["survey"] = survey
        return data

    def create(self, validated_data):
        version_name = validated_data["version_name"]
        version_code = validated_data["version_code"]
        survey_pk = self.context["survey_pk"]

        # Retrieve the survey
        try:
            survey = Survey.objects.get(pk=survey_pk)
        except Survey.DoesNotExist:
            raise NotFound(f"Survey with id {survey_pk} not found.")

        # Serialize the survey data using SurveyDetailSerializer
        survey_data_serializer = SurveyDetailsSerializer(survey)
        survey_data = survey_data_serializer.data
        del survey_data["versions"]

        # Create the SurveyVersion
        survey_version = SurveyVersion.objects.create(
            survey=survey,
            version_name=version_name,
            version_code=version_code,
            body=survey_data,
        )
        return survey_version
