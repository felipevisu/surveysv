from rest_framework import serializers

from surveysv.surveys.models import Survey


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


from rest_framework import serializers


class SurveyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ["id", "title"]

    def update(self, instance, validated_data):

        # Update the survey fields
        instance.title = validated_data.get("title", instance.title)
        instance.save()

        return instance
