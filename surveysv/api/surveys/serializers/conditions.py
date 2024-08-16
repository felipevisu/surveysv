from rest_framework import serializers

from surveysv.surveys.models import Condition, SurveyQuestion


class ConditionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ["primary_question", "conditional_question", "operator", "value"]

    def validate(self, data):
        survey_id = self.context["survey_pk"]
        primary_question = data["primary_question"]
        conditional_question = data["conditional_question"]

        # Check if both questions are assigned to the survey
        if not SurveyQuestion.objects.filter(
            survey_id=survey_id, question=primary_question
        ).exists():
            raise serializers.ValidationError(
                f"Primary question {primary_question} is not assigned to survey {survey_id}."
            )

        if not SurveyQuestion.objects.filter(
            survey_id=survey_id, question=conditional_question
        ).exists():
            raise serializers.ValidationError(
                f"Conditional question {conditional_question} is not assigned to survey {survey_id}."
            )

        # Check if the primary question is of type 'MULTIPLE_CHOICE' or 'SELECT'
        if primary_question.type not in ["MULTIPLE_CHOICE", "SELECT"]:
            raise serializers.ValidationError(
                "Primary question must be of type 'MULTIPLE_CHOICE' or 'SELECT'."
            )

        return data


class ConditionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ["operator", "value"]

    def update(self, instance: Condition, validated_data):
        instance.operator = validated_data.get("operator", instance.operator)
        instance.value = validated_data.get("value", instance.value)
        instance.save()

        return instance
