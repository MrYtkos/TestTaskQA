from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status
from rest_framework.viewsets import ModelViewSet
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['answers'] = AnswerSerializer(instance.answers.all(), many=True).data
        logger.info(f"Получен вопрос с ID {instance.id} и связанные ответы")
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        logger.info(f"Удалён вопрос с ID {instance.id} и связанные ответы")
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True, url_path='answers')
    def create_answer(self, request, pk=None):
        question = self.get_object()
        serializer = AnswerSerializer(data=request.data, context={'question': question})
        serializer.is_valid(raise_exception=True)
        serializer.save(question=question)
        logger.info(f"Создан ответ для вопроса с ID {pk} от пользователя {request.data.get('user_id')}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnswerViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        answer = get_object_or_404(Answer, id=pk)
        serializer = AnswerSerializer(answer)
        logger.info(f"Получен ответ с ID {answer.id}")
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        answer = get_object_or_404(Answer, pk=pk)
        answer.delete()
        logger.info(f"Удален ответ с ID {answer.id}")
        return Response(status=status.HTTP_204_NO_CONTENT)
