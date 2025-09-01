from rest_framework import serializers
from questions.models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {'question': {'read_only': True}}

    def validate_text(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError('Please enter text.')
        return value

    def validate_user_id(self, value: str) -> str:
        if not str(value).strip():
            raise serializers.ValidationError('Идентификатор пользователя не может быть пустым')
        return value


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def validate_text(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError('Вопрос не может быть пустым')
        return value
