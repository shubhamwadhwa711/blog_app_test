from rest_framework import serializers

from apps.blog import models


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Writer
        fields = ('id', 'first_name', 'last_name', 'is_editor')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = '__all__'
