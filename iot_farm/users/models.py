from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from iot_farm.models import AppAbstractBaseModel
from .validators import MobileValidator


# Create your models here.
class AppAbstractUser(AbstractUser, AppAbstractBaseModel):
    """
    An abstract base class implementing a fully featured User model with admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    mobile_validator = MobileValidator()

    email = models.EmailField(
        _('email address'), unique=True, blank=False, null=False, help_text=_('Required. For notifying users.'),
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    address = models.CharField(_('address'), max_length=200, blank=True, null=True, help_text=_('User address'))
    mobile = models.CharField(_('mobile'), max_length=12, blank=False, null=False, validators=[mobile_validator], )
    avatar = models.ImageField(_('avatar'), upload_to='images/avatars/', max_length=500, blank=True, null=True,
                               help_text=_('User avatar'))

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True


class User(AppAbstractUser):
    """
    Users within the Django authentication system are represented by this model.
    Username and password are required. Other fields are optional.
    """

    class Meta(AppAbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
