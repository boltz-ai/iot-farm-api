from django.db import models
from django.utils.translation import gettext_lazy as _

from iot_farm.models import AppAbstractBaseModel
from users.models import User
from . import settings as farm_settings


# Create your models here.
class Sensor(AppAbstractBaseModel):
    """
    The Request model.
    """
    ON = farm_settings.ON
    OFF = farm_settings.OFF
    AUTO = farm_settings.AUTO
    MANUAL = farm_settings.MANUAL

    STATUS_CHOICES = farm_settings.STATUS_CHOICES
    MODE_CHOICES = farm_settings.MODE_CHOICES

    device = models.CharField(_('device'), max_length=50, blank=False, null=False, help_text=_('Required'), )
    parameter = models.CharField(_('parameter'), max_length=20, blank=False, null=False, help_text=_('Required'), )
    value = models.FloatField(_('value'), blank=False, null=False, help_text=_('Required'))
    status = models.CharField(_('status'), choices=STATUS_CHOICES, default=ON, max_length=3, blank=False, null=False,
                              help_text=_('The status of device, `ON` or `OFF`. Default: `ON`'))
    mode = models.CharField(_('mode'), choices=MODE_CHOICES, default=AUTO, max_length=6, blank=False, null=False,
                            help_text=_('The mode of device, `AUTO` or `MANUAL`. Default: `AUTO`'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, help_text=_('Required.'), )

    def __str__(self):
        return self.device

    class Meta:
        verbose_name = _('sensor')
        verbose_name_plural = _('sensors')
