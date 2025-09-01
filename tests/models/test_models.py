import pytest
from django.utils import timezone
from questions.models import Question, Answer
import uuid


@pytest.mark.django_db
class TestQuestionModel:
    def test_create_question(self):
        question = Question.objects.create(text="What is Python?")
        assert question.id is not None
        assert question.text == "What is Python?"
        assert question.created_at <= timezone.now()

    def test_question_str(self):
        question = Question.objects.create(text="What is Python?")
        assert question.text == "What is Python?"[:50]


@pytest.mark.django_db
class TestAnswerModel:
    def test_create_answer(self):
        question = Question.objects.create(text="What is Python?")
        answer = Answer.objects.create(
            question=question,
            user_id=str(uuid.uuid4()),
            text="Python is a programming language."
        )
        assert answer.id is not None
        assert answer.question == question
        assert answer.text == "Python is a programming language."
        assert answer.created_at <= timezone.now()

    def test_answer_str(self):
        question = Question.objects.create(text="What is Python?")
        answer = Answer.objects.create(
            question=question,
            user_id=str(uuid.uuid4()),
            text="Python is a programming language."
        )
        assert answer.text == "Python is a programming language."[:50]

    def test_answer_cascade_delete(self):
        question = Question.objects.create(text="What is Python?")
        answer = Answer.objects.create(
            question=question,
            user_id=str(uuid.uuid4()),
            text="Python is a programming language."
        )
        question.delete()
        assert Answer.objects.count() == 0
