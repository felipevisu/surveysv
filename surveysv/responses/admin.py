from django.contrib import admin

from .models import Answer, Response


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ["survey", "id", "created", "updated"]
    search_fields = ["survey__title"]
    list_filter = ["survey", "created"]
    date_hierarchy = "created"

    def has_add_permission(self, request, obj=None):
        return False  # Disable adding new Responses from the admin


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["response", "question", "body"]
    search_fields = ["question__body", "body"]
    list_filter = ["question", "response__survey"]
