from email.policy import default

from django.db import models
from ordered_model.models import OrderedModel

from ..core.models import ModelWithDates


class QuestionType(models.TextChoices):
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    SELECT = "SELECT"
    TEXT = "TEXT"


class Question(ModelWithDates):
    body = models.TextField()
    type = models.CharField(choices=QuestionType.choices)
    required = models.BooleanField(default=False)
    reusable = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.body} ({self.get_type_display()})"


class Option(OrderedModel):
    title = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    question = models.ForeignKey(
        Question, related_name="options", on_delete=models.CASCADE
    )
    goal = models.PositiveIntegerField(null=True, blank=True, default=None)

    class Meta:
        unique_together = ("question", "value")
        ordering = ["order"]

    def __str__(self) -> str:
        return self.title


class Operator(models.TextChoices):
    IS_EQUAL = "IS_EQUAL"
    IS_DIFERENT = "IS_DIFERENT"
    CONTAINS = "CONTAINS"
    NOT_CONTAINS = "NOT_CONTAINS"


class Condition(models.Model):
    primary_question = models.ForeignKey(
        Question, related_name="childrens", on_delete=models.CASCADE
    )
    conditional_question = models.ForeignKey(
        Question, related_name="conditions", on_delete=models.CASCADE
    )
    operator = models.CharField(max_length=50, choices=Operator.choices)
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


class SurveyVersion(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name="versions"
    )
    created = models.DateTimeField(auto_now_add=True)
    version_name = models.CharField(max_length=25)
    version_code = models.SlugField(max_length=25)
    body = models.JSONField()

    class Meta:
        unique_together = ("survey", "version_code")
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"{self.survey.title} - {self.version_code}"
