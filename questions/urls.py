from django.urls import path, include
from rest_framework import routers
from questions.views import QuestionViewSet, AnswerViewSet

router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'answers', AnswerViewSet, basename='answer')

urlpatterns = [
    path('', include(router.urls)),
]
