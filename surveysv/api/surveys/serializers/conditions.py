from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from surveysv.surveys.models import Condition


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ["id", "primary_question", "operator", "value"]

    def validate_primary_question(self, value):
        if value.type not in ["SELECT", "MULTIPLE_CHOICE"]:
            raise ValidationError(
                "Primary question must be of type 'SELECT' or 'MULTIPLE_CHOICE'."
            )
        return value

    def update(self, instance, validated_data):
        # Ensure the primary question is of a valid type
        primary_question = validated_data.get(
            "primary_question", instance.primary_question
        )
        if primary_question.type not in ["SELECT", "MULTIPLE_CHOICE"]:
            raise ValidationError(
                "Primary question must be of type 'SELECT' or 'MULTIPLE_CHOICE'."
            )

        # Update the instance with the validated data
        instance.conditional_question = validated_data.get(
            "conditional_question", instance.conditional_question
        )
        instance.operator = validated_data.get("operator", instance.operator)
        instance.value = validated_data.get("value", instance.value)
        instance.save()

        return instance
