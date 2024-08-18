from rest_framework import serializers
from rest_framework.exceptions import NotFound

from surveysv.surveys.models import Option, Question


class OptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["title", "value", "goal"]

    def validate(self, data):
        question_pk = self.context["question_pk"]
        try:
            question = Question.objects.get(pk=question_pk)
        except Question.DoesNotExist:
            raise NotFound(f"Question with id {question_pk} does not exist.")
        # Check if an Option with the same question and value already exists
        if Option.objects.filter(question=question, value=data["value"]).exists():
            raise serializers.ValidationError(
                f"An option with value '{data['value']}' already exists for this question."
            )
        data["question"] = question
        return data


class OptionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["title", "value", "goal"]


class OptionBulkDeleteSerializer(serializers.Serializer):
    option_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    def validate_option_ids(self, value):
        # Ensure the list is not empty
        if not value:
            raise serializers.ValidationError("This field cannot be empty.")

        # Check if all IDs exist in the database
        existing_ids = set(
            Option.objects.filter(id__in=value).values_list("id", flat=True)
        )
        non_existent_ids = set(value) - existing_ids

        if non_existent_ids:
            raise serializers.ValidationError(
                f"No options found with IDs: {sorted(non_existent_ids)}"
            )

        return value
