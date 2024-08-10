from django.contrib import admin

from .models import Condition, Goal, Option, Question, Survey, SurveyQuestion


class OptionInline(admin.TabularInline):
    model = Option
    extra = 0


class ConditionInline(admin.TabularInline):
    model = Condition
    fk_name = "primary_question"
    extra = 0


class GoalInline(admin.TabularInline):
    model = Goal
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("body", "type", "required")
    inlines = [OptionInline, ConditionInline, GoalInline]


class SurveyQuestionInline(admin.TabularInline):
    model = SurveyQuestion
    extra = 0


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [SurveyQuestionInline]


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ("survey", "question", "order", "page_number")
    list_filter = ("survey", "page_number")
