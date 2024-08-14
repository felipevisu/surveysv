from django.urls import path

from .views import (
    ConditionCreateAPIView,
    ConditionDeleteAPIView,
    ConditionUpdateAPIView,
    OptionBulkDeleteAPIView,
    OptionCreateAPIView,
    OptionDeleteAPIView,
    OptionUpdateAPIView,
    QuestionDeleteAPIView,
    QuestionUpdateAPIView,
    SurveyCreateAPIView,
    SurveyDeleteAPIView,
    SurveyQuestionCreateAPIView,
    SurveyUpdateAPIView,
)

urlpatterns = [
    path("create/", SurveyCreateAPIView.as_view(), name="survey-create"),
    path("<int:pk>/update/", SurveyUpdateAPIView.as_view(), name="survey-update"),
    path("<int:pk>/delete/", SurveyDeleteAPIView.as_view(), name="survey-delete"),
    path(
        "questions/<int:survey_pk>/create/",
        SurveyQuestionCreateAPIView.as_view(),
        name="question-create",
    ),
    path(
        "questions/<int:pk>/update/",
        QuestionUpdateAPIView.as_view(),
        name="question-update",
    ),
    path(
        "questions/<int:pk>/delete/",
        QuestionDeleteAPIView.as_view(),
        name="question-delete",
    ),
    path(
        "conditions/<int:question_pk>/create/",
        ConditionCreateAPIView.as_view(),
        name="condition-create",
    ),
    path(
        "conditions/<int:pk>/update/",
        ConditionUpdateAPIView.as_view(),
        name="condition-update",
    ),
    path(
        "conditions/<int:pk>/delete/",
        ConditionDeleteAPIView.as_view(),
        name="condition-delete",
    ),
    path(
        "options/<int:question_pk>/create/",
        OptionCreateAPIView.as_view(),
        name="option-create",
    ),
    path(
        "options/<int:pk>/update/", OptionUpdateAPIView.as_view(), name="option-update"
    ),
    path(
        "options/<int:pk>/delete/", OptionDeleteAPIView.as_view(), name="option-delete"
    ),
    path("options/delete/", OptionBulkDeleteAPIView.as_view(), name="option-delete"),
]
