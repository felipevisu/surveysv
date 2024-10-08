import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from surveysv.surveys.models import Condition, Question, Survey


@pytest.mark.django_db
def test_create_condition(
    api_client, user, survey: Survey, question: Question, question_2: Question
):
    api_client.force_authenticate(user=user)

    primary_question = question
    conditional_question = question_2

    survey.questions.add(primary_question, conditional_question)

    # Prepare the data for creating a new condition
    data = {
        "primary_question": primary_question.id,
        "conditional_question": conditional_question.id,
        "operator": "IS_EQUAL",
        "value": "blue",
    }

    # Send a POST request to create the condition
    response = api_client.post(
        reverse("condition-create", args=[survey.id]), data, format="json"
    )

    # Assert the response status code is 201 (Created)
    assert response.status_code == 201

    # Assert the condition was created correctly
    assert Condition.objects.count() == 1
    condition = Condition.objects.get(primary_question=question)
    assert condition.primary_question == primary_question
    assert condition.conditional_question == conditional_question
    assert condition.operator == "IS_EQUAL"
    assert condition.value == "blue"


@pytest.mark.django_db
def test_create_condition_with_questions_not_in_the_survey(
    api_client, user, survey, question, question_2
):
    api_client.force_authenticate(user=user)

    primary_question = question
    conditional_question = question_2

    # Prepare the data for creating a new condition
    data = {
        "primary_question": primary_question.id,
        "conditional_question": conditional_question.id,
        "operator": "IS_EQUAL",
        "value": "blue",
    }

    # Send a POST request to create the condition
    response = api_client.post(
        reverse("condition-create", args=[survey.id]), data, format="json"
    )

    # Assert the response status code is 400 (Error)
    assert response.status_code == 400
    content = response.json()
    error = content["non_field_errors"][0]
    message = "Primary question What is your favorite color? (Multiple Choice) is not assigned to survey"
    assert message in error


@pytest.mark.django_db
def test_update_condition(api_client, user, condition):
    api_client.force_authenticate(user=user)

    # Prepare the data to update the condition
    data = {
        "operator": "IS_DIFERENT",
        "value": "red",
    }

    # Send a PUT request to update the condition
    response = api_client.put(
        reverse("condition-update", args=[condition.id]), data, format="json"
    )

    # Assert the response status code is 200 (OK)
    assert response.status_code == 200

    # Refresh from the database and assert the condition was updated correctly
    condition.refresh_from_db()
    assert condition.operator == "IS_DIFERENT"
    assert condition.value == "red"


@pytest.mark.django_db
def test_delete_condition(api_client, user, condition):
    api_client.force_authenticate(user=user)

    # Send a DELETE request to remove the condition
    response = api_client.delete(reverse("condition-delete", args=[condition.id]))

    # Assert the response status code is 204 (No Content)
    assert response.status_code == 204

    # Assert the condition was deleted
    assert Condition.objects.count() == 0
