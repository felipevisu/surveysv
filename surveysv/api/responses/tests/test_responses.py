import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from surveysv.responses.models import Answer, Response
from surveysv.surveys.models import Option


@pytest.mark.django_db
def test_create_valid_response(api_client, user, movie_survey):
    api_client.force_authenticate(user=user)

    # Prepare data for a valid response
    data = {
        "survey": movie_survey.id,
        "answers": [
            {
                "question": movie_survey.questions.get(
                    body="What is your favorite movie genre?"
                ).id,
                "body": "comedy",
            },
            {
                "question": movie_survey.questions.get(
                    body="Which actor do you prefer?"
                ).id,
                "body": "leonardo",
            },
            {
                "question": movie_survey.questions.get(
                    body="How many movies do you watch per month?"
                ).id,
                "body": "5",
            },
            {
                "question": movie_survey.questions.get(
                    body="What's your favorite Comedy movie?"
                ).id,
                "body": "superbad",
            },
        ],
    }

    # Send POST request to create the response
    response = api_client.post(reverse("response-create"), data, format="json")

    # Check the response status code
    assert response.status_code == status.HTTP_201_CREATED
    assert Response.objects.count() == 1
    assert Answer.objects.count() == 4


@pytest.mark.django_db
def test_create_response_with_condition_met(api_client, user, movie_survey):
    api_client.force_authenticate(user=user)

    # Prepare data where conditions are met (comedy selected, so the comedy movie question should be answered)
    data = {
        "survey": movie_survey.id,
        "answers": [
            {
                "question": movie_survey.questions.get(
                    body="What is your favorite movie genre?"
                ).id,
                "body": "comedy",
            },
            {
                "question": movie_survey.questions.get(
                    body="Which actor do you prefer?"
                ).id,
                "body": "leonardo",
            },
            {
                "question": movie_survey.questions.get(
                    body="How many movies do you watch per month?"
                ).id,
                "body": "5",
            },
            {
                "question": movie_survey.questions.get(
                    body="What's your favorite Comedy movie?"
                ).id,
                "body": "superbad",
            },
        ],
    }

    # Send POST request to create the response
    response = api_client.post(reverse("response-create"), data, format="json")

    # Check the response status code
    assert response.status_code == status.HTTP_201_CREATED
    assert Response.objects.count() == 1
    assert Answer.objects.count() == 4


@pytest.mark.django_db
def test_create_response_with_goal_reached(api_client, user, movie_survey):
    api_client.force_authenticate(user=user)

    question_1 = movie_survey.questions.get(body="What is your favorite movie genre?")
    option_comedy = question_1.options.get(value="comedy")

    # Simulate 5 responses selecting "Comedy" to reach the goal
    for _ in range(option_comedy.goal):
        Answer.objects.create(
            question=question_1,
            body="comedy",
            response=Response.objects.create(survey=movie_survey),
        )

    # Prepare data where the goal is already reached for "comedy"
    data = {
        "survey": movie_survey.id,
        "answers": [
            {
                "question": movie_survey.questions.get(
                    body="What is your favorite movie genre?"
                ).id,
                "body": "comedy",
            },
            {
                "question": movie_survey.questions.get(
                    body="Which actor do you prefer?"
                ).id,
                "body": "leonardo",
            },
            {
                "question": movie_survey.questions.get(
                    body="How many movies do you watch per month?"
                ).id,
                "body": "5",
            },
        ],
    }

    # Send POST request to create the response
    response = api_client.post(reverse("response-create"), data, format="json")

    # Check the response status code (expect failure due to goal reached)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert "The option 'comedy' for question with id" in str(
        response.data["non_field_errors"][0]
    )


@pytest.mark.django_db
def test_create_response_missing_required_question(api_client, user, movie_survey):
    api_client.force_authenticate(user=user)

    # Prepare data missing a required question (e.g., missing "How many movies do you watch per month?")
    data = {
        "survey": movie_survey.id,
        "answers": [
            {
                "question": movie_survey.questions.get(
                    body="What is your favorite movie genre?"
                ).id,
                "body": "comedy",
            },
            {
                "question": movie_survey.questions.get(
                    body="Which actor do you prefer?"
                ).id,
                "body": "leonardo",
            },
        ],
    }

    # Send POST request to create the response
    response = api_client.post(reverse("response-create"), data, format="json")

    # Check the response status code (expect failure due to missing required question)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Required question with id" in str(response.data["non_field_errors"][0])


@pytest.mark.django_db
def test_create_response_with_condition_not_met(api_client, user, movie_survey):
    api_client.force_authenticate(user=user)

    # Prepare data where conditions are not met (e.g., drama selected, but answer for comedy movie is given)
    data = {
        "survey": movie_survey.id,
        "answers": [
            {
                "question": movie_survey.questions.get(
                    body="What is your favorite movie genre?"
                ).id,
                "body": "drama",
            },
            {
                "question": movie_survey.questions.get(
                    body="Which actor do you prefer?"
                ).id,
                "body": "leonardo",
            },
            {
                "question": movie_survey.questions.get(
                    body="How many movies do you watch per month?"
                ).id,
                "body": "5",
            },
            {
                "question": movie_survey.questions.get(
                    body="What's your favorite Comedy movie?"
                ).id,
                "body": "superbad",
            },
        ],
    }

    # Send POST request to create the response
    response = api_client.post(reverse("response-create"), data, format="json")

    # Check the response status code (expect failure due to condition not being met)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "answer should not be provided" in str(response.data["non_field_errors"][0])
