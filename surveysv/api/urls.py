from django.urls import include, path

urlpatterns = [
    path("surveys/", include("surveysv.api.surveys.urls"), name="surveys"),
    path("responses/", include("surveysv.api.responses.urls"), name="responses"),
]
