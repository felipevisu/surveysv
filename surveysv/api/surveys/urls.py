from django.urls import path

from . import views

urlpatterns = [
    path("", views.SurveyListAPIView.as_view(), name="survey-list"),
    path("create/", views.SurveyCreateAPIView.as_view(), name="survey-create"),
    path("<int:pk>/update/", views.SurveyUpdateAPIView.as_view(), name="survey-update"),
    path(
        "<int:pk>/details/", views.SurveyDetailsAPIView.as_view(), name="survey-details"
    ),
    path("<int:pk>/delete/", views.SurveyDeleteAPIView.as_view(), name="survey-delete"),
    path(
        "questions/<int:survey_pk>/create/",
        views.SurveyQuestionCreateAPIView.as_view(),
        name="question-create",
    ),
    path(
        "questions/<int:pk>/update/",
        views.QuestionUpdateAPIView.as_view(),
        name="question-update",
    ),
    path(
        "questions/<int:pk>/delete/",
        views.QuestionDeleteAPIView.as_view(),
        name="question-delete",
    ),
    path(
        "/conditions/<int:survey_pk>/create/",
        views.ConditionCreateAPIView.as_view(),
        name="condition-create",
    ),
    path(
        "conditions/<int:pk>/update/",
        views.ConditionUpdateAPIView.as_view(),
        name="condition-update",
    ),
    path(
        "conditions/<int:pk>/delete/",
        views.ConditionDeleteAPIView.as_view(),
        name="condition-delete",
    ),
    path(
        "options/<int:question_pk>/create/",
        views.OptionCreateAPIView.as_view(),
        name="option-create",
    ),
    path(
        "options/<int:pk>/update/",
        views.OptionUpdateAPIView.as_view(),
        name="option-update",
    ),
    path(
        "options/<int:pk>/delete/",
        views.OptionDeleteAPIView.as_view(),
        name="option-delete",
    ),
    path(
        "options/delete/", views.OptionBulkDeleteAPIView.as_view(), name="option-delete"
    ),
]
