from rest_framework import serializers

from surveysv.surveys.models import Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "title", "value", "question", "goal"]


class OptionBulkDeleteSerializer(serializers.Serializer):
    option_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    def validate_option_ids(self, value):
        if not value:
            raise serializers.ValidationError("This field cannot be empty.")
        return value
