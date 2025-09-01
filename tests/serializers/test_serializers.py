import pytest
from questions.serializers import QuestionSerializer, AnswerSerializer
from questions.models import Question, Answer
import uuid


@pytest.mark.django_db
class TestQuestionSerializer:
    def test_valid_question(self):
        data = {"text": "What is Python?"}
        serializer = QuestionSerializer(data=data)
        assert serializer.is_valid()
        question = serializer.save()
        assert question.text == "What is Python?"

    def test_invalid_question_empty_text(self):
        data = {"text": ""}
        serializer = QuestionSerializer(data=data)
        assert not serializer.is_valid()
        assert "text" in serializer.errors


@pytest.mark.django_db
class TestAnswerSerializer:
    def test_valid_answer(self):
        question = Question.objects.create(text="What is Python?")
        data = {
            "user_id": str(uuid.uuid4()),
            "text": "Python is a programming language."
        }
        serializer = AnswerSerializer(data=data, context={'question': question})
        assert serializer.is_valid()
        answer = serializer.save(question=question)
        assert answer.text == "Python is a programming language."
        assert answer.question == question

    def test_invalid_answer_empty_text(self):
        question = Question.objects.create(text="What is Python?")
        data = {"user_id": str(uuid.uuid4()), "text": ""}
        serializer = AnswerSerializer(data=data, context={'question_id': question.id})
        assert not serializer.is_valid()
        assert "text" in serializer.errors

    def test_invalid_answer_no_user_id(self):
        question = Question.objects.create(text="What is Python?")
        data = {"text": "Python is a programming language."}
        serializer = AnswerSerializer(data=data, context={'question_id': question.id})
        assert not serializer.is_valid()
        assert "user_id" in serializer.errors
