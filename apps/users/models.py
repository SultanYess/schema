import uuid
import uuid as _uuid
from django.db import models
from django.contrib.auth import models as django_auth_models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from apps.common.mixins import models as mixin_models
from apps.common.mixins.utils import IINRegexValidator


def get_post_photo_path(instance, filename):
    return f"photo_{instance.id}/photo/{filename}"


class User(
    mixin_models.FullNameModel,
    mixin_models.TimestampModel,
    django_auth_models.AbstractUser,
):
    id: _uuid.UUID = models.UUIDField(
        primary_key=True,
        default=_uuid.uuid4,
        unique=True,
        editable=False,
        name="id",
        verbose_name=_("UUID identification"),
    )
    is_developer = models.BooleanField(verbose_name=_("Is Developer"), default=False)
    iin: str = models.CharField(
        max_length=12,
        unique=True,
        validators=[IINRegexValidator()],
        verbose_name=_("IIN"),
        null=True,
        blank=False,
    )
    date_of_birth = models.DateField(
        null=True, blank=False, verbose_name=_("Date of Birth")
    )
    phone = PhoneNumberField(
        max_length=12, blank=True, null=False, verbose_name=_("Phone")
    )
    address = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("Address")
    )
