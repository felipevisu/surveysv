from optparse import Option

from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from surveysv.responses.models import Answer, Response
from surveysv.surveys.models import Question, Survey


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["question", "body"]


class ResponseCreateSerializer(serializers.ModelSerializer):
    answers = AnswerCreateSerializer(many=True)

    class Meta:
        model = Response
        fields = ["survey", "answers"]

    def _check_option_goal(self, question, selected_option_value):
        """
        Check if the selected option's goal has been reached, if applicable.
        """
        try:
            selected_option = question.options.get(value=selected_option_value)
        except Option.DoesNotExist:
            raise ValidationError(
                f"Selected option with value '{selected_option_value}' does not exist for question with id {question.id}."
            )

        if selected_option.goal is not None:
            current_count = Answer.objects.filter(
                question=question, body=selected_option_value
            ).count()
            if current_count >= selected_option.goal:
                raise ValidationError(
                    f"The option '{selected_option_value}' for question with id {question.id} has reached its goal and cannot be selected anymore."
                )

    def _check_condition_satisfaction(self, question, answers_dict):
        """
        Check if the conditions for the question are satisfied based on the answers provided.
        """
        conditions = question.conditions.all()
        for condition in conditions:
            primary_question_answer = answers_dict.get(
                condition.primary_question.id, None
            )
            if primary_question_answer is not None:
                if (
                    condition.operator == "IS_EQUAL"
                    and primary_question_answer != condition.value
                ):
                    return False
                elif (
                    condition.operator == "IS_DIFFERENT"
                    and primary_question_answer == condition.value
                ):
                    return False
                elif (
                    condition.operator == "CONTAINS"
                    and condition.value not in primary_question_answer
                ):
                    return False
                elif (
                    condition.operator == "NOT_CONTAINS"
                    and condition.value in primary_question_answer
                ):
                    return False
        return True

    def validate(self, data):
        survey = data.get("survey")
        answers = data.get("answers")
        answers_dict = {answer["question"].id: answer["body"] for answer in answers}

        # Check if the survey exists
        if not Survey.objects.filter(pk=survey.id).exists():
            raise NotFound(f"Survey with id {survey.id} does not exist.")

        # Check each answer
        for answer in answers:
            question = answer.get("question")
            body = answer.get("body")
            # Check if the question exists
            if not Question.objects.filter(pk=question.id).exists():
                raise ValidationError(f"Question with id {question.id} does not exist.")

            # Check if the question is assigned to the survey
            if not survey.questions.filter(pk=question.id).exists():
                raise ValidationError(
                    f"Question with id {question.id} is not assigned to the survey with id {survey.id}."
                )

            # Check if the option's goal is reached (if applicable)
            if question.type in ["MULTIPLE_CHOICE", "SELECT"]:
                self._check_option_goal(question, body)

            # Check if the question has conditions and if they are satisfied
            if question.conditions.exists():
                if not self._check_condition_satisfaction(question, answers_dict):
                    raise ValidationError(
                        f"Condition for question with id {question.id} is not satisfied, so an answer should not be provided."
                    )

            # Check if the required question has an empty body (if no condition or condition is satisfied)
            if question.required:
                condition_satisfied = self._check_condition_satisfaction(
                    question, answers_dict
                )
                if condition_satisfied and not body.strip():
                    raise ValidationError(
                        f"Answer to required question with id {question.id} cannot be empty."
                    )

        # Check if all required questions have been answered (considering conditions)
        required_questions = survey.questions.filter(required=True)
        for required_question in required_questions:
            condition_satisfied = self._check_condition_satisfaction(
                required_question, answers_dict
            )
            if condition_satisfied and required_question.id not in answers_dict:
                raise ValidationError(
                    f"Required question with id {required_question.id} is missing from the answers."
                )

        return data

    def create(self, validated_data):
        answers_data = validated_data.pop("answers")
        response = Response.objects.create(**validated_data)

        # Create each answer associated with the response
        for answer_data in answers_data:
            Answer.objects.create(response=response, **answer_data)

        return response
