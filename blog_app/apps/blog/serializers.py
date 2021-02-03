from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions, status

from apps.blog import models

User = get_user_model()


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Writer
        fields = ('id', 'first_name', 'last_name', 'is_editor')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = '__all__'
        read_only_fields = ('written_by', 'edited_by', 'status')


class EditorArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = '__all__'
        read_only_fields = ('written_by', 'edited_by')


class ArticleStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ('id', 'status', 'edited_by')
        read_only_fields = ('edited_by',)


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)
    custom_error = {
        'authentication_error': _('Invalid Credentials.'),
        'inactive_user': _('The account is not active, contact the admin.')
    }

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                raise exceptions.AuthenticationFailed(detail={"error": self.custom_error['authentication_error']})
            if not user.is_active:
                raise serializers.ValidationError({"inactive_user": self.custom_error['inactive_user']},
                                                  code=status.HTTP_403_FORBIDDEN)
            if not hasattr(user, 'writer'):
                raise serializers.ValidationError(
                    {"invalid_writer_account": _('No writer found associated to this account.')})
        else:
            raise exceptions.NotAuthenticated()
        attrs['user'] = user
        return attrs
