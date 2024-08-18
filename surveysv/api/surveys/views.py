from django.db.models import Count
from rest_framework import filters, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ...surveys.models import Condition, Option, Question, Survey, SurveyQuestion
from .serializers import (
    ConditionCreateSerializer,
    ConditionUpdateSerializer,
    OptionBulkDeleteSerializer,
    OptionCreateSerializer,
    OptionUpdateSerializer,
    QuestionUpdateSerializer,
    SurveyCreateSerializer,
    SurveyDetailsSerializer,
    SurveyListSerializer,
    SurveyQuestionCreateSerializer,
    SurveyUpdateSerializer,
)


class SurveyListAPIView(generics.ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created", "title"]
    ordering = ["created"]

    def get_queryset(self):
        return Survey.objects.annotate(question_count=Count("surveyquestion"))


class SurveyDetailsAPIView(generics.RetrieveAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyDetailsSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Survey.objects.select_related().prefetch_related(
            # Prefetch related questions (SurveyQuestion)
            "surveyquestion_set__question",
            # Prefetch conditions for each question
            "surveyquestion_set__question__conditions",
            # Prefetch options for each question
            "surveyquestion_set__question__options",
        )


class SurveyCreateAPIView(generics.CreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyCreateSerializer


class SurveyUpdateAPIView(generics.UpdateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyUpdateSerializer


class SurveyDeleteAPIView(generics.DestroyAPIView):
    queryset = Survey.objects.all()
    lookup_field = "pk"


class SurveyQuestionCreateAPIView(generics.CreateAPIView):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionCreateSerializer

    def perform_create(self, serializer: SurveyQuestionCreateSerializer):
        survey_id = self.kwargs["survey_pk"]  # Extract survey primary key from the URL
        try:
            survey = Survey.objects.get(pk=survey_id)
        except Survey.DoesNotExist:
            raise ValidationError(f"Survey with id {survey_id} does not exist.")

        # Pass the survey instance to the serializer
        serializer.save(survey=survey)


class QuestionUpdateAPIView(generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionUpdateSerializer
    lookup_field = "pk"


class QuestionDeleteAPIView(generics.DestroyAPIView):
    queryset = Question.objects.all()
    lookup_field = "pk"


class OptionCreateAPIView(generics.CreateAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Retrieve the question based on the pk in the URL
        try:
            question = Question.objects.get(pk=self.kwargs["question_pk"])
        except Question.DoesNotExist:
            raise ValidationError(
                f"Question with id {self.kwargs['question_pk']} does not exist."
            )

        # Add the question to the context
        context["question"] = question
        return context


class OptionUpdateAPIView(generics.UpdateAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionUpdateSerializer
    lookup_field = "pk"


class OptionDeleteAPIView(generics.DestroyAPIView):
    queryset = Option.objects.all()
    lookup_field = "pk"


class OptionBulkDeleteAPIView(generics.GenericAPIView):
    serializer_class = OptionBulkDeleteSerializer

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        option_ids = serializer.validated_data["option_ids"]
        deleted, _ = Option.objects.filter(id__in=option_ids).delete()

        return Response({"deleted": deleted}, status=status.HTTP_204_NO_CONTENT)


class ConditionCreateAPIView(generics.CreateAPIView):
    queryset = Condition.objects.all()
    serializer_class = ConditionCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["survey_pk"] = self.kwargs["survey_pk"]
        return context


class ConditionUpdateAPIView(generics.UpdateAPIView):
    queryset = Condition.objects.all()
    serializer_class = ConditionUpdateSerializer
    lookup_field = "pk"


class ConditionDeleteAPIView(generics.DestroyAPIView):
    queryset = Condition.objects.all()
    lookup_field = "pk"
