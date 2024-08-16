from rest_framework import serializers

from surveysv.surveys.models import Option


class OptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["title", "value", "goal"]

    def validate(self, data):
        question = self.context["question"]
        # Check if an Option with the same question and value already exists
        if Option.objects.filter(question=question, value=data["value"]).exists():
            raise serializers.ValidationError(
                f"An option with value '{data['value']}' already exists for this question."
            )
        return data

    def create(self, validated_data):
        # Get the question from the context
        question = self.context["question"]
        # Create the option
        return Option.objects.create(question=question, **validated_data)


class OptionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["title", "value", "goal"]


class OptionBulkDeleteSerializer(serializers.Serializer):
    option_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    def validate_option_ids(self, value):
        if not value:
            raise serializers.ValidationError("This field cannot be empty.")
        return value
