from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Writer(User):
    is_editor = models.BooleanField(_('Is Editor'), default=False)

    class Meta:
        verbose_name = _('Writer')
        verbose_name_plural = _('Writers')

    def __str__(self):
        return self.get_full_name()


class Article(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    article_status = ((PENDING, PENDING),
                      (APPROVED, APPROVED),
                      (REJECTED, REJECTED))
    title = models.CharField(_('Title'), max_length=255)
    content = models.TextField(_('Content'))
    status = models.CharField(_('Status'), choices=article_status, default=PENDING, max_length=100)
    written_by = models.ForeignKey(Writer, on_delete=models.CASCADE, related_name="written_by")
    edited_by = models.ForeignKey(Writer, on_delete=models.SET_NULL, related_name="edited_by", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    def __str__(self):
        return self.title
