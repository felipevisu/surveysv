from rest_framework import generics, status
from rest_framework.response import Response

from ...surveys.models import Condition, Option, Question, Survey, SurveyQuestion
from .serializers import (
    ConditionSerializer,
    OptionBulkDeleteSerializer,
    OptionSerializer,
    QuestionUpdateSerializer,
    SurveyCreateSerializer,
    SurveyQuestionCreateSerializer,
    SurveyUpdateSerializer,
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


class QuestionUpdateAPIView(generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionUpdateSerializer
    lookup_field = "pk"


class QuestionDeleteAPIView(generics.DestroyAPIView):
    queryset = Question.objects.all()
    lookup_field = "pk"


class OptionCreateAPIView(generics.CreateAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class OptionUpdateAPIView(generics.UpdateAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
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
    serializer_class = ConditionSerializer


class ConditionUpdateAPIView(generics.UpdateAPIView):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    lookup_field = "pk"


class ConditionDeleteAPIView(generics.DestroyAPIView):
    queryset = Condition.objects.all()
    lookup_field = "pk"
