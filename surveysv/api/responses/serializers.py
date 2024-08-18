from rest_framework import serializers

from surveysv.responses.models import Answer, Response


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["question", "body"]


class ResponseCreateSerializer(serializers.ModelSerializer):
    answers = AnswerCreateSerializer(many=True)

    class Meta:
        model = Response
        fields = ["survey", "answers"]

    def create(self, validated_data):
        answers_data = validated_data.pop("answers")
        response = Response.objects.create(**validated_data)

        # Create each answer associated with the response
        for answer_data in answers_data:
            Answer.objects.create(response=response, **answer_data)

        return response
