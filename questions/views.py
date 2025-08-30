from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework import generics, mixins, viewsets
from rest_framework.viewsets import ModelViewSet


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=True, methods=['post'])
    def answers(self, request, pk=None):
        question = self.get_object()
        serializer = AnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(question=question)
        return Response(serializer.data)


class AnswerViewSet(mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
