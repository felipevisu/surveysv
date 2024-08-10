from rest_framework import serializers

from surveysv.surveys.models import Option, Question, SurveyQuestion


class OptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["title", "value"]


class SurveyQuestionCreateSerializer(serializers.ModelSerializer):
    body = serializers.CharField(source="question.body", write_only=True)
    type = serializers.CharField(source="question.type", write_only=True)
    required = serializers.BooleanField(
        source="question.required", write_only=True, required=False
    )
    options = OptionCreateSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = SurveyQuestion
        fields = [
            "survey",
            "body",
            "type",
            "required",
            "order",
            "page_number",
            "options",
        ]

    def create(self, validated_data):
        # Extract the question data from the validated data
        question_data = validated_data.pop("question")
        options_data = validated_data.pop("options", [])
        question, created = Question.objects.get_or_create(**question_data)

        # Create the SurveyQuestion instance
        survey_question = SurveyQuestion.objects.create(
            question=question, **validated_data
        )

        # Create the options if any
        for order, option_data in enumerate(options_data, start=1):
            Option.objects.create(question=question, order=order, **option_data)

        return survey_question


class QuestionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ["id", "body", "type", "required"]

    def update(self, instance, validated_data):
        # Update the instance fields with the validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the instance after all fields are updated
        instance.save()

        return instance
