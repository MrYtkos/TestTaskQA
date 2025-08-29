from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet


class QuestionViewSet(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
