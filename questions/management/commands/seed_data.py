from django.core.management.base import BaseCommand
from questions.models import Question, Answer
import uuid


class Command(BaseCommand):
    help = "Seed database with test Questions and Answers"

    def handle(self, *args, **kwargs):
        # Очистим старые данные
        Answer.objects.all().delete()
        Question.objects.all().delete()

        # Создаём вопросы
        q1 = Question.objects.create(text="Что такое Django?")
        q2 = Question.objects.create(text="Что такое FastAPI?")
        q3 = Question.objects.create(text="Чем отличается SQL от NoSQL?")

        # Создаём ответы
        Answer.objects.create(question=q1, user_id=uuid.uuid4(),
                              text="Django — это Python-фреймворк для веб-приложений.")
        Answer.objects.create(question=q1, user_id=uuid.uuid4(), text="Используется для серверного рендеринга и API.")

        Answer.objects.create(question=q2, user_id=uuid.uuid4(),
                              text="FastAPI — современный фреймворк для API на Python.")
        Answer.objects.create(question=q2, user_id=uuid.uuid4(),
                              text="Отличается высокой скоростью и простотой аннотаций.")

        Answer.objects.create(question=q3, user_id=uuid.uuid4(),
                              text="SQL — это реляционные базы данных с жёсткой схемой.")
        Answer.objects.create(question=q3, user_id=uuid.uuid4(),
                              text="NoSQL — документные/ключ-значение базы, более гибкие.")

        self.stdout.write(self.style.SUCCESS("✅ База успешно заполнена тестовыми вопросами и ответами"))
