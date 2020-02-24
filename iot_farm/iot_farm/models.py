import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AppAbstractBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), blank=True, null=True)
    deleted_at = models.DateTimeField(_('deleted at'), blank=True, null=True)

    class Meta:
        abstract = True


class NameDescriptionAbstractBaseModel(models.Model):
    name = models.CharField(_('name'), max_length=200, blank=False, null=False, help_text=_('Required.'), )
    description = models.TextField(_('description'), blank=True, null=True, help_text=_('Description'), )

    class Meta:
        abstract = True
