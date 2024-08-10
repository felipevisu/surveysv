import pytest
from django.urls import reverse

from surveysv.surveys.models import Survey


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
