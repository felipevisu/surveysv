from django.db import models

from surveysv.core.models import ModelWithDates
from surveysv.surveys.models import Question, Survey


class Response(ModelWithDates):
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)

    class Meta:
        pass

    def __str__(self) -> str:
        return f"{self.survey} - {self.pk}"


class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    body = models.TextField()

    def __str__(self) -> str:
        return self.body
