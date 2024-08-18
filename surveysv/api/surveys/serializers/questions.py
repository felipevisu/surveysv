from rest_framework import serializers
from rest_framework.exceptions import NotFound

from surveysv.surveys.models import Condition, Option, Question, Survey, SurveyQuestion


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ["primary_question", "operator", "value"]


class OptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["title", "value", "goal"]


class SurveyQuestionCreateSerializer(serializers.ModelSerializer):
    body = serializers.CharField(source="question.body", write_only=True)
    type = serializers.CharField(source="question.type", write_only=True)
    required = serializers.BooleanField(
        source="question.required", write_only=True, required=False
    )
    reusable = serializers.BooleanField(
        source="question.reusable", write_only=True, required=False
    )
    options = OptionCreateSerializer(many=True, write_only=True, required=False)
    conditions = ConditionSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = SurveyQuestion
        fields = [
            "body",
            "type",
            "required",
            "reusable",
            "order",
            "page_number",
            "options",
            "conditions",
        ]

    def validate(self, data):
        survey_pk = self.context["survey_pk"]
        try:
            survey = Survey.objects.get(pk=survey_pk)
        except Survey.DoesNotExist:
            raise NotFound(f"Survey with id {survey_pk} does not exist.")

        # Pass the survey instance to the serializer
        data["survey"] = survey
        return data

    def validate_conditions(self, conditions):
        for condition in conditions:
            primary_question_id = condition["primary_question"].id
            primary_question = Question.objects.get(id=primary_question_id)

            if primary_question.type not in ["SELECT", "MULTIPLE_CHOICE"]:
                raise serializers.ValidationError(
                    f"Primary question with ID {primary_question_id} must be of type 'SELECT' or 'MULTIPLE_CHOICE'."
                )
        return conditions

    def create(self, validated_data):
        # Extract the question data from the validated data
        question_data = validated_data.pop("question")
        options_data = validated_data.pop("options", [])
        conditions_data = validated_data.pop("conditions", [])
        question, created = Question.objects.get_or_create(**question_data)

        # Create the SurveyQuestion instance
        survey_question = SurveyQuestion.objects.create(
            question=question, **validated_data
        )

        # Create the options if any
        for order, option_data in enumerate(options_data, start=1):
            Option.objects.create(question=question, order=order, **option_data)

        # Create the conditions if any
        for condition_data in conditions_data:
            Condition.objects.create(conditional_question=question, **condition_data)

        return survey_question


class QuestionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ["id", "body", "type", "required", "reusable"]

    def update(self, instance: Question, validated_data):
        # Update the instance fields with the validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the instance after all fields are updated
        instance.save()

        return instance
