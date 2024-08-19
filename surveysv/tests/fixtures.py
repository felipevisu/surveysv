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


import pytest

from surveysv.surveys.models import Condition, Option, Question, Survey


@pytest.fixture
def movie_survey():
    # Create the survey
    survey = Survey.objects.create(title="Ultimate Movie Preferences Survey")

    # Create questions
    question_1 = Question.objects.create(
        body="What is your favorite movie genre?",
        type="SELECT",
        required=True,
    )
    question_2 = Question.objects.create(
        body="Which actor do you prefer?",
        type="MULTIPLE_CHOICE",
        required=True,
    )
    question_3 = Question.objects.create(
        body="How many movies do you watch per month?",
        type="TEXT",
        required=True,
    )
    question_4 = Question.objects.create(
        body="Do you enjoy watching movies with subtitles?",
        type="SELECT",
        required=False,
    )
    # New Questions for Favorite Movies by Genre
    question_5_comedy = Question.objects.create(
        body="What's your favorite Comedy movie?",
        type="SELECT",
        required=False,
    )
    question_5_drama = Question.objects.create(
        body="What's your favorite Drama movie?",
        type="SELECT",
        required=False,
    )
    question_5_action = Question.objects.create(
        body="What's your favorite Action movie?",
        type="SELECT",
        required=False,
    )

    # Add options to multiple choice and select questions
    option_1_1 = Option.objects.create(
        question=question_1,
        title="Action",
        value="action",
        goal=5,
    )
    option_1_2 = Option.objects.create(
        question=question_1,
        title="Comedy",
        value="comedy",
        goal=5,
    )
    option_1_3 = Option.objects.create(
        question=question_1,
        title="Drama",
        value="drama",
        goal=5,
    )
    option_2_1 = Option.objects.create(
        question=question_2, title="Leonardo DiCaprio", value="leonardo"
    )
    option_2_2 = Option.objects.create(
        question=question_2, title="Meryl Streep", value="meryl"
    )
    option_2_3 = Option.objects.create(
        question=question_2, title="Tom Hanks", value="tom"
    )
    option_4_1 = Option.objects.create(question=question_4, title="Yes", value="yes")
    option_4_2 = Option.objects.create(question=question_4, title="No", value="no")

    # Options for Favorite Movies by Genre
    option_5_comedy_1 = Option.objects.create(
        question=question_5_comedy, title="The Hangover", value="hangover"
    )
    option_5_comedy_2 = Option.objects.create(
        question=question_5_comedy, title="Superbad", value="superbad"
    )
    option_5_comedy_3 = Option.objects.create(
        question=question_5_comedy, title="Step Brothers", value="step_brothers"
    )
    option_5_comedy_4 = Option.objects.create(
        question=question_5_comedy, title="Anchorman", value="anchorman"
    )
    option_5_drama_1 = Option.objects.create(
        question=question_5_drama, title="The Godfather", value="godfather"
    )
    option_5_drama_2 = Option.objects.create(
        question=question_5_drama, title="Forrest Gump", value="forrest_gump"
    )
    option_5_drama_3 = Option.objects.create(
        question=question_5_drama, title="Shawshank Redemption", value="shawshank"
    )
    option_5_drama_4 = Option.objects.create(
        question=question_5_drama, title="Schindler's List", value="schindlers_list"
    )
    option_5_action_1 = Option.objects.create(
        question=question_5_action, title="Die Hard", value="die_hard"
    )
    option_5_action_2 = Option.objects.create(
        question=question_5_action, title="Mad Max: Fury Road", value="mad_max"
    )
    option_5_action_3 = Option.objects.create(
        question=question_5_action, title="The Dark Knight", value="dark_knight"
    )
    option_5_action_4 = Option.objects.create(
        question=question_5_action, title="Gladiator", value="gladiator"
    )

    # Add conditions
    Condition.objects.create(
        primary_question=question_1,
        conditional_question=question_5_comedy,
        operator="IS_EQUAL",
        value="comedy",
    )
    Condition.objects.create(
        primary_question=question_1,
        conditional_question=question_5_drama,
        operator="IS_EQUAL",
        value="drama",
    )
    Condition.objects.create(
        primary_question=question_1,
        conditional_question=question_5_action,
        operator="IS_EQUAL",
        value="action",
    )

    # Associate questions with the survey
    survey.questions.add(
        question_1,
        question_2,
        question_3,
        question_4,
        question_5_comedy,
        question_5_drama,
        question_5_action,
    )

    return survey
