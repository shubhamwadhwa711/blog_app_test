from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from apps.blog import serializers, models


class ArticleAPIView(ModelViewSet):
    serializer_class = serializers.ArticleSerializer
    queryset = models.Article.objects.all()
