from datetime import datetime,timedelta

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        }
    )
    phone_number = models.CharField(verbose_name=_('phone_number'), max_length=11, blank=True)
    email = models.EmailField(_('email address'), blank=True, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.and change .'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        """Return the short name for the user."""
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserOTP(models.Model):
    SIGNUP = 1
    LOGIN = 2
    EMAIL = 3
    CODE_TYPE_CHOICE = (
        (SIGNUP, _("sing up")),
        (LOGIN, _('LOGIN')),
        (EMAIL, _('email')),
    )

    code = models.CharField(verbose_name=_('code'), max_length=6)
    expire_time_start = models.DateTimeField(verbose_name=_("start of expire time"), default=datetime.now,
                                             null=True)
    expire_time_end = models.DateTimeField(_("end of expire time"), default=(datetime.now() +  timedelta(minutes = 5)),null=True)
    code_type = models.IntegerField(_("code type"), choices=CODE_TYPE_CHOICE, null=True)
    phone_number = models.CharField(_('phone number'), max_length=11, null=True)
    email = models.EmailField(verbose_name=_('email'), null=True)

    def time_in_range(self,): 

        """Return true if x is in the range [start, end]"""
        if self.expire_time_end< timezone.now():
            return True
        else:
            return False