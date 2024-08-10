import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from surveysv.surveys.models import Option, Question, Survey


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
def question():
    return Question.objects.create(
        body="What is your favorite color?", type="MULTIPLE_CHOICE", required=True
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
            Option(title="Red", value="red", question=question, order=1),
            Option(title="Blue", value="blue", question=question, order=2),
            Option(title="Green", value="green", question=question, order=3),
        ]
    )
