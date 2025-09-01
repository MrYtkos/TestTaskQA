import uuid

from django.db import models


class Question(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    user_id = models.UUIDField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
