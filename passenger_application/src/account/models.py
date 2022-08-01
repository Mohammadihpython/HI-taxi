from datetime import datetime
from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
import datetime


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        max_length=11,
        unique=True,

    )
    username = models.CharField(
        null=True,
        blank=True,
        max_length=250,
    )

    first_name = models.CharField(
        max_length=250,
        verbose_name=_("first name"),
        null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length=250,
        verbose_name=_("last name")
    )
    objects = UserManager()
    EMAIL_FIELD = None
    USERNAME_FIELD = 'phone_number'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def send_email(self, subject, mesage, from_email, **kwargs):
        """
        Send an email to this user.
        """
        send_mail(subject, mesage, from_email, [self.email], **kwargs)


class UserOTP(models.Model):
    SINGUP = 1

    LOGIN = 2
    SMS = 4
    OTP_TYPE_CHOICE = (
        (SINGUP, _('Signup')),
        (LOGIN, _('Login')),
        (SMS, _('sms')),
    )
    code = models.CharField(verbose_name=_('code'), max_length=6)
    expire_time_start = models.DateTimeField(
        verbose_name=_("start of expire time"),
        default=datetime.datetime.now,

    )
    expire_time_end = models.DateTimeField(
        _("end of the expire time"),
        default=datetime.timedelta(minutes=5)
    )
    code_type = models.IntegerField(
        verbose_name=_("code type"),
        choices=OTP_TYPE_CHOICE,
        null=True
    )
    phone_number = models.CharField(_("phone number"), max_length=11)

    def time_in_range(self, start, end, x):
        """ return tur if x is in the range[start,end]"""
        if start <= x <= end:
            return True
        else:
            return False
