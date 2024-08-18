from rest_framework import serializers

from surveysv.surveys.models import Condition, Option, Question, Survey, SurveyQuestion


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ["id", "operator", "value", "primary_question"]


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "title", "value", "goal"]


class QuestionSerializer(serializers.ModelSerializer):
    conditions = ConditionSerializer(many=True, read_only=True)
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "body", "type", "required", "reusable", "conditions", "options"]


class SurveyQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = SurveyQuestion
        fields = ["id", "order", "page_number", "question"]


class SurveyDetailsSerializer(serializers.ModelSerializer):
    questions = SurveyQuestionSerializer(
        many=True, read_only=True, source="surveyquestion_set"
    )

    class Meta:
        model = Survey
        fields = ["id", "title", "created", "updated", "questions"]
