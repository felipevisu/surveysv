import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from surveysv.surveys.models import Condition, Option, Question, Survey, SurveyVersion


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create(username="admin", password="surveysv")


@pytest.fixture
def survey():
    return Survey.objects.create(title="Survey")


@pytest.fixture
def survey_version(survey):
    return SurveyVersion.objects.create(
        survey=survey, version_name="Version 1", version_code="version-1", body={}
    )


@pytest.fixture
def question():
    return Question.objects.create(
        body="What is your favorite color?", type="MULTIPLE_CHOICE", required=True
    )


@pytest.fixture
def question_2():
    return Question.objects.create(
        body="What is your favorite movie?", type="MULTIPLE_CHOICE", required=True
    )


@pytest.fixture
def condition(question, question_2):
    return Condition.objects.create(
        primary_question=question,
        conditional_question=question_2,
        operator="IS_EQUAL",
        value="blue",
    )


@pytest.fixture
def option(question):
    return Option.objects.create(
        title="Original Option", value="original_value", order=1, question=question
    )


@pytest.fixture
def option_list(question):
    return Option.objects.bulk_create(
        [
            Option(title="Red", value="red", question=question),
            Option(title="Blue", value="blue", question=question),
            Option(title="Green", value="green", question=question),
        ]
    )
