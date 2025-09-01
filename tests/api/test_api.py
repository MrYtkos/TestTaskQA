import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from questions.models import Question, Answer
import uuid


@pytest.mark.django_db
class TestQuestionAPI:
    def setup_method(self):
        self.client = APIClient()
        self.question_data = {"text": "What is Python?"}
        self.question = Question.objects.create(text=self.question_data["text"])

    def test_get_questions_list(self):
        response = self.client.get(reverse('question-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        assert response.data[0]["text"] == self.question_data["text"]

    def test_create_question(self):
        data = {"text": "What is Django?"}
        response = self.client.post(reverse('question-list'), data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Question.objects.count() == 2
        assert Question.objects.last().text == data["text"]

    def test_create_question_empty_text(self):
        data = {"text": ""}
        response = self.client.post(reverse('question-list'), data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_question_detail(self):
        answer = Answer.objects.create(
            question=self.question,
            user_id=str(uuid.uuid4()),
            text="Python is a programming language."
        )
        response = self.client.get(reverse('question-detail', args=[self.question.id]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["text"] == self.question_data["text"]
        assert "answers" in response.data
        assert len(response.data["answers"]) == 1
        assert response.data["answers"][0]["text"] == answer.text

    def test_get_question_detail_no_answers(self):
        response = self.client.get(reverse('question-detail', args=[self.question.id]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["text"] == self.question_data["text"]
        assert response.data["answers"] == []

    def test_delete_question_cascades_answers(self):
        answer = Answer.objects.create(
            question=self.question,
            user_id=str(uuid.uuid4()),
            text="Python is a programming language."
        )
        response = self.client.delete(reverse('question-detail', args=[self.question.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Question.objects.count() == 0
        assert Answer.objects.count() == 0


@pytest.mark.django_db
class TestAnswerAPI:
    def setup_method(self):
        self.client = APIClient()
        self.question = Question.objects.create(text="What is Python?")
        self.user_id = uuid.uuid4()
        self.answer_data = {
            "user_id": str(self.user_id),
            "text": "Python is a programming language."
        }

    def test_create_answer(self):
        Answer.objects.all().delete()
        question_id = int(self.question.id)
        response = self.client.post(
            reverse('question-create-answer', args=[question_id]),
            self.answer_data,
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Answer.objects.count() == 1
        assert Answer.objects.last().text == self.answer_data["text"]
        assert Answer.objects.last().user_id == self.user_id
        assert Answer.objects.last().question == self.question

    def test_create_answer_nonexistent_question(self):
        response = self.client.post(
            "/questions/999/answers/",
            self.answer_data,
            format='json'
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_answer_empty_text(self):
        data = {"user_id": self.user_id, "text": ""}
        response = self.client.post(
            reverse('question-create-answer', args=[self.question.id]),
            data,
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_answer_invalid_user_id(self):
        data = {"user_id": "", "text": "Python is a programming language."}
        response = self.client.post(
            reverse('question-create-answer', args=[self.question.id]),
            data,
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_answer(self):
        answer = Answer.objects.create(
            question=self.question,
            user_id=self.user_id,
            text=self.answer_data["text"]
        )
        response = self.client.get(reverse('answer-detail', args=[answer.id]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["text"] == self.answer_data["text"]
        assert response.data["user_id"] == str(self.user_id)

    def test_get_answer_nonexistent(self):
        response = self.client.get(reverse('answer-detail', args=[999]))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_answer(self):
        answer = Answer.objects.create(
            question=self.question,
            user_id=self.user_id,
            text=self.answer_data["text"]
        )
        response = self.client.delete(reverse('answer-detail', args=[answer.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Answer.objects.count() == 0

    def test_delete_answer_nonexistent(self):
        response = self.client.delete(reverse('answer-detail', args=[999]))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_answers_not_allowed(self):
        response = self.client.post(
            "/answers/",
            self.answer_data,
            format='json'
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
