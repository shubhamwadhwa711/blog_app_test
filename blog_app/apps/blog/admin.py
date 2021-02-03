from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from apps.blog import models


@admin.register(models.Writer)
class WriterModelAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'username', 'email', 'is_editor')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    add_form = UserCreationForm
    list_display = ('id', 'first_name', 'last_name', 'is_active', 'is_editor')
    search_fields = ('email', 'first_name', 'last_name')
    list_editable = ('is_editor',)


@admin.register(models.Article)
class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'written_by', 'status')
    list_editable = ('status',)
