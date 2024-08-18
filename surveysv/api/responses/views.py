from rest_framework import generics

from surveysv.responses.models import Response

from .serializers import ResponseCreateSerializer


class ResponseCreateAPIView(generics.CreateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseCreateSerializer
