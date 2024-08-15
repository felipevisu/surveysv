import pytest
from django.urls import reverse

from surveysv.surveys.models import Question, Survey, SurveyQuestion


@pytest.mark.django_db
def test_survey_list_with_question_count(api_client, user):
    api_client.force_authenticate(user=user)

    # Create a few surveys
    survey1 = Survey.objects.create(title="Survey 1")
    survey2 = Survey.objects.create(title="Survey 2")

    # Create questions associated with the surveys
    question1 = Question.objects.create(
        body="Question 1", type="MULTIPLE_CHOICE", required=True
    )
    question2 = Question.objects.create(body="Question 2", type="TEXT", required=True)
    SurveyQuestion.objects.create(survey=survey1, question=question1)
    SurveyQuestion.objects.create(survey=survey1, question=question2)
    SurveyQuestion.objects.create(survey=survey2, question=question1)

    # Send a GET request to list the surveys
    response = api_client.get(reverse("survey-list"))

    # Assert the response status code is 200 (OK)
    assert response.status_code == 200

    # Check the response data
    response_data = response.json()

    assert len(response_data["results"]) == 2

    survey1_data = response_data["results"][0]
    survey2_data = response_data["results"][1]

    # Verify the question counts
    assert survey1_data["question_count"] == 2
    assert survey2_data["question_count"] == 1

    # Verify other fields
    assert survey1_data["title"] == "Survey 1"
    assert "created" in survey1_data
    assert "updated" in survey1_data


@pytest.mark.django_db
def test_create_survey_(api_client, user):
    api_client.force_authenticate(user=user)

    # Prepare the data for creating a new survey with the child survey
    data = {"title": "Main Survey"}

    # Send a POST request to create the survey
    response = api_client.post(reverse("survey-create"), data, format="json")

    # Assert the response status code
    assert response.status_code == 201

    # Assert the survey was created correctly
    assert Survey.objects.count() == 1  # Main survey + child survey


@pytest.mark.django_db
def test_update_survey(api_client, user, survey):
    api_client.force_authenticate(user=user)

    # Prepare the data to update the survey, adding new child surveys and removing others
    data = {
        "title": "Updated Survey Title",
    }

    # Send a PUT request to update the survey
    response = api_client.put(
        reverse("survey-update", args=[survey.id]), data, format="json"
    )

    # Assert the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert the survey was updated correctly
    survey.refresh_from_db()
    assert survey.title == "Updated Survey Title"


@pytest.mark.django_db
def test_delete_survey(api_client, user, survey):
    api_client.force_authenticate(user=user)

    # Send a DELETE request to delete the survey
    response = api_client.delete(reverse("survey-delete", args=[survey.id]))

    # Assert the response status code is 204 (No Content)
    assert response.status_code == 204

    # Assert the survey was deleted
    assert Survey.objects.count() == 0
