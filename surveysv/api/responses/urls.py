from django.urls import path

from .views import ResponseCreateAPIView

urlpatterns = [
    path("create/", ResponseCreateAPIView.as_view(), name="response-create"),
]
