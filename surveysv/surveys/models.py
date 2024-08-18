from typing import Any

from django.db import models
from ordered_model.models import OrderedModel

from ..core.models import ModelWithDates


class QuestionType:
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    SELECT = "SELECT"
    TEXT = "TEXT"

    CHOICES = [(MULTIPLE_CHOICE, "Multiple Choice"), (SELECT, "Select"), (TEXT, "Text")]


class Question(ModelWithDates):
    body = models.TextField()
    type = models.CharField(choices=QuestionType.CHOICES)
    required = models.BooleanField(blank=True, null=True)
    reusable = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self) -> str:
        return f"{self.body} ({self.get_type_display()})"


class Option(OrderedModel):
    title = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    question = models.ForeignKey(
        Question, related_name="options", on_delete=models.CASCADE
    )
    goal = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ("question", "value")
        ordering = ["order"]

    def __str__(self) -> str:
        return self.title


class Operator:
    IS_EQUAL = "IS_EQUAL"
    IS_DIFERENT = "IS_DIFERENT"
    CONTAINS = "CONTAINS"
    NOT_CONTAINS = "NOT_CONTAINS"

    CHOICES = [
        (IS_EQUAL, "Is equal"),
        (IS_DIFERENT, "Is diferent"),
        (CONTAINS, "Contains"),
        (NOT_CONTAINS, "Not contains"),
    ]


class Condition(models.Model):
    primary_question = models.ForeignKey(
        Question, related_name="childrens", on_delete=models.CASCADE
    )
    conditional_question = models.ForeignKey(
        Question, related_name="conditions", on_delete=models.CASCADE
    )
    operator = models.CharField(max_length=50, choices=Operator.CHOICES)
    value = models.TextField()


class Survey(ModelWithDates):
    title = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question, through="SurveyQuestion")

    def __str__(self) -> str:
        return self.title


class SurveyQuestion(OrderedModel):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    page_number = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("survey", "question")
        ordering = ["order"]
