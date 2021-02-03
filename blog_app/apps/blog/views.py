from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from apps.blog import serializers, models
from apps.blog.permissions import IsEditor


class ArticleAPIView(ModelViewSet):
    serializer_class = serializers.ArticleSerializer
    queryset = models.Article.objects.all()

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        if self.request.user.writer.is_editor:
            serializer = serializers.EditorArticleSerializer
        return serializer

    def perform_create(self, serializer):
        serializer.save(written_by=self.request.user.writer)


class ArticleStatusAPIView(mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = (IsEditor,)
    serializer_class = serializers.ArticleStatusUpdateSerializer
    queryset = models.Article.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(status__in=['pending', 'rejected'])
        return qs

    def perform_update(self, serializer):
        serializer.save(edited_by=self.request.user.writer)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class UserLoginAPI(GenericViewSet):
    serializer_class = serializers.AuthTokenSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_data = serializers.WriterSerializer(user.writer).data
        data = {'token': token.key, 'user': user_data}
        return Response(data, status=HTTP_200_OK)
