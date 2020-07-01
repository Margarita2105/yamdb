from rest_framework import serializers

from .models import Review, Comment, Title


class TitleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Comment
        