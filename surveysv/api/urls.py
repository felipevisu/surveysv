from django.urls import include, path

urlpatterns = [
    path("surveys/", include("surveysv.api.surveys.urls"), name="surveys"),
]
