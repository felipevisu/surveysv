import pytest
from django.urls import reverse

from surveysv.surveys.models import Option


@pytest.mark.django_db
def test_create_option(api_client, user, question):
    api_client.force_authenticate(user=user)

    # Prepare the data for creating a new option
    data = {
        "title": "New Option",
        "value": "new_option_value",
    }

    # Send a POST request to create the option
    response = api_client.post(
        reverse("option-create", args=[question.id]), data, format="json"
    )

    # Assert the response status code is 201 (Created)
    assert response.status_code == 201

    # Assert the option was created correctly
    assert Option.objects.count() == 1
    option = Option.objects.get(question=question)
    assert option.title == "New Option"
    assert option.value == "new_option_value"


@pytest.mark.django_db
def test_create_option_with_existent_value(api_client, user, question, option_list):
    api_client.force_authenticate(user=user)

    # Prepare the data for creating a new option
    data = {
        "title": "Green",
        "value": "green",
    }

    # Send a POST request to create the option
    response = api_client.post(
        reverse("option-create", args=[question.id]), data, format="json"
    )

    # Assert the response status code is 400 (Error)
    assert response.status_code == 400

    content = response.json()
    error = content["non_field_errors"][0]
    message = "An option with value 'green' already exists for this question."
    assert error == message


@pytest.mark.django_db
def test_update_option(api_client, user, option):
    api_client.force_authenticate(user=user)

    # Prepare the data to update the option
    data = {
        "title": "Updated Option",
        "value": "updated_value",
        "question": option.question.id,
    }

    # Send a PUT request to update the option
    response = api_client.put(
        reverse("option-update", args=[option.id]), data, format="json"
    )

    # Assert the response status code is 200 (OK)
    assert response.status_code == 200

    # Refresh from database and assert the option was updated correctly
    option.refresh_from_db()
    assert option.title == "Updated Option"
    assert option.value == "updated_value"


@pytest.mark.django_db
def test_delete_option(api_client, user, option):
    api_client.force_authenticate(user=user)

    # Send a DELETE request to remove the option
    response = api_client.delete(reverse("option-delete", args=[option.id]))

    # Assert the response status code is 204 (No Content)
    assert response.status_code == 204

    # Assert the option was deleted
    assert Option.objects.count() == 0


@pytest.mark.django_db
def test_delete_options(api_client, user, option_list):
    api_client.force_authenticate(user=user)

    option1, option2, option3 = option_list

    # Prepare the data to delete options
    data = {"option_ids": [option1.id, option2.id]}

    # Send a DELETE request to remove the options
    response = api_client.delete(reverse("option-delete"), data, format="json")

    # Assert the response status code is 204 (No Content)
    assert response.status_code == 204

    # Assert the options were deleted correctly
    assert Option.objects.count() == 1
    assert Option.objects.filter(id=option3.id).exists()
