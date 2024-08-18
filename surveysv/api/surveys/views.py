from django.db.models import Count
from rest_framework import filters, generics, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from ...surveys.models import (
    Condition,
    Option,
    Question,
    Survey,
    SurveyQuestion,
    SurveyVersion,
)
from .serializers import (
    ConditionCreateSerializer,
    ConditionUpdateSerializer,
    OptionBulkDeleteSerializer,
    OptionCreateSerializer,
    OptionUpdateSerializer,
    QuestionUpdateSerializer,
    SurveyCreateSerializer,
    SurveyDetailsSerializer,
    SurveyGenerateVersionSerializer,
    SurveyListSerializer,
    SurveyQuestionCreateSerializer,
    SurveyUpdateSerializer,
    SurveyVersionSerializer,
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
            "versions",
            "surveyquestion_set__question",
            "surveyquestion_set__question__conditions",
            "surveyquestion_set__question__options",
        )


class SurveyVersionDetailView(generics.RetrieveAPIView):
    serializer_class = SurveyVersionSerializer
    lookup_field = "version_code"

    def get_object(self):
        survey_pk = self.kwargs["survey_pk"]
        version_code = self.kwargs["version_code"]
        try:
            return SurveyVersion.objects.get(
                survey_id=survey_pk, version_code=version_code
            )
        except SurveyVersion.DoesNotExist:
            raise NotFound(
                f"SurveyVersion with survey_pk={survey_pk} and version_code={version_code} not found."
            )


class SurveyCreateAPIView(generics.CreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyCreateSerializer


class SurveyGenerateVersionAPIView(generics.CreateAPIView):
    serializer_class = SurveyGenerateVersionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Add the survey to the context
        context["survey_pk"] = self.kwargs["survey_pk"]
        return context


class SurveyVersionDeleteAPIView(generics.DestroyAPIView):
    queryset = SurveyVersion.objects.all()

    def get_object(self):
        survey_pk = self.kwargs["survey_pk"]
        version_code = self.kwargs["version_code"]

        try:
            survey_version = SurveyVersion.objects.get(
                survey_id=survey_pk, version_code=version_code
            )
        except SurveyVersion.DoesNotExist:
            raise NotFound(
                f"SurveyVersion with survey_pk={survey_pk} and version_code={version_code} not found."
            )

        return survey_version


class SurveyLatestVersionAPIView(generics.RetrieveAPIView):
    serializer_class = SurveyVersionSerializer

    def get_object(self):
        survey_pk = self.kwargs["survey_pk"]

        # Retrieve the survey to ensure it exists
        try:
            survey = Survey.objects.get(pk=survey_pk)
        except Survey.DoesNotExist:
            raise NotFound(f"Survey with id {survey_pk} not found.")

        # Retrieve the latest SurveyVersion for the given survey
        latest_version = (
            SurveyVersion.objects.filter(survey_id=survey_pk)
            .order_by("-created")
            .first()
        )

        if not latest_version:
            raise NotFound(f"No versions found for Survey with id {survey_pk}.")

        return latest_version


class SurveyUpdateAPIView(generics.UpdateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyUpdateSerializer


class SurveyDeleteAPIView(generics.DestroyAPIView):
    queryset = Survey.objects.all()
    lookup_field = "pk"


class SurveyQuestionCreateAPIView(generics.CreateAPIView):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Add the question to the context
        context["survey_pk"] = self.kwargs["survey_pk"]
        return context


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
        # Add the question to the context
        context["question_pk"] = self.kwargs["question_pk"]
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
