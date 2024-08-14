import pytest
from django.urls import reverse

from surveysv.surveys.models import Condition, Option, Question, SurveyQuestion


@pytest.mark.django_db
def test_create_survey_question_with_options(api_client, user, survey):
    api_client.force_authenticate(user=user)

    # Prepare the data for creating a new question linked to the survey
    data = {
        "body": "What is your favorite color?",
        "type": "MULTIPLE_CHOICE",
        "required": True,
        "page_number": 1,
        "options": [
            {"title": "Red", "value": "red"},
            {"title": "Blue", "value": "blue"},
            {"title": "Green", "value": "green"},
        ],
    }

    # Send a POST request to create the survey question with options
    response = api_client.post(
        reverse("question-create", args=[survey.id]), data, format="json"
    )

    # Assert the response status code is 201 (Created)
    assert response.status_code == 201

    # Assert the survey question was created correctly
    assert SurveyQuestion.objects.count() == 1
    assert Question.objects.count() == 1
    assert Option.objects.count() == 3

    # Fetch the created SurveyQuestion instance
    survey_question = SurveyQuestion.objects.get(survey=survey)

    # Assert that the survey question has the correct attributes
    assert survey_question.question.body == "What is your favorite color?"
    assert survey_question.question.type == "MULTIPLE_CHOICE"
    assert survey_question.question.required is True
    assert survey_question.order == 0
    assert survey_question.page_number == 1

    # Assert that the options were created correctly
    options = survey_question.question.options.all()
    assert options.count() == 3
    assert options.filter(title="Red", value="red").exists()
    assert options.filter(title="Blue", value="blue").exists()
    assert options.filter(title="Green", value="green").exists()


@pytest.mark.django_db
def test_create_survey_question_with_conditions(
    api_client, user, survey, question, option_list
):
    api_client.force_authenticate(user=user)

    primary_question = question

    # Prepare the data for creating a new question linked to the survey, with conditions
    data = {
        "body": "Why do you like red?",
        "type": "MULTIPLE_CHOICE",
        "required": True,
        "page_number": 1,
        "options": [
            {"title": "Love", "value": "love"},
            {"title": "Blood", "value": "blood"},
        ],
        "conditions": [
            {
                "primary_question": primary_question.id,
                "operator": "IS_EQUAL",
                "value": "red",
            }
        ],
    }

    # Send a POST request to create the survey question with options and conditions
    response = api_client.post(
        reverse("question-create", args=[survey.id]), data, format="json"
    )

    assert Question.objects.count() == 2  # Original primary question + new question
    assert Option.objects.count() == 5
    assert Condition.objects.count() == 1

    # Assert the response status code is 201 (Created)
    assert response.status_code == 201

    # Assert that the condition was created correctly
    condition = Condition.objects.get(primary_question=question)
    created_question = Question.objects.get(body="Why do you like red?")
    assert condition.conditional_question == created_question
    assert condition.operator == "IS_EQUAL"
    assert condition.value == "red"


@pytest.mark.django_db
def test_update_question(api_client, user, question):
    api_client.force_authenticate(user=user)

    # Prepare the data to update the question
    data = {
        "body": "Updated question text?",
        "type": "SELECT",
        "required": False,
    }

    # Send a PUT request to update the question
    response = api_client.put(
        reverse("question-update", args=[question.id]), data, format="json"
    )

    # Assert the response status code is 200 (OK)
    assert response.status_code == 200

    # Refresh from database
    question.refresh_from_db()

    # Assert the question was updated correctly
    assert question.body == "Updated question text?"
    assert question.type == "SELECT"
    assert question.required is False


@pytest.mark.django_db
def test_delete_question(api_client, user, question):
    api_client.force_authenticate(user=user)

    # Send a DELETE request to delete the survey
    response = api_client.delete(reverse("question-delete", args=[question.id]))

    # Assert the response status code is 204 (No Content)
    assert response.status_code == 204

    # Assert the survey was deleted
    assert Question.objects.count() == 0
