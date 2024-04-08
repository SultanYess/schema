import uuid as _uuid
from django.db import models
from typing import List
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from apps.common.mixins import models as mixin_models
from django.contrib.postgres import fields as postgres_fields

User = get_user_model()


def get_user_fr_image_path(instance, filename):
    return f"user_{instance.id}/face_recognition_images/{filename}"


class OriginalImage(mixin_models.TimestampModel):
    """Оригинальные изображения"""

    id: _uuid.UUID = models.UUIDField(
        primary_key=True,
        default=_uuid.uuid4,
        unique=True,
        editable=False,
        name="id",
        verbose_name=_("UUID identification"),
    )
    original_image: models.ImageField = models.ImageField(
        upload_to=get_user_fr_image_path,
        null=False,
        blank=False,
        verbose_name=_("Original image"),
    )

    created_by: User = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="fr_original_images",
        verbose_name=_("Created by"),
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = _("Original image")
        verbose_name_plural = _("Original images")


class RecognizedFace(mixin_models.TimestampModel):
    """Распознанные лица"""

    id: _uuid.UUID = (
        models.UUIDField(
            primary_key=True,
            default=_uuid.uuid4,
            unique=True,
            editable=False,
            name="id",
            verbose_name=_("UUID identification"),
        ),
    )

    original_image_id: _uuid.UUID
    original_image: OriginalImage = models.ForeignKey(
        OriginalImage,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="recognized_faces",
        verbose_name=_("Original image"),
    )

    face_image: str = models.TextField(
        null=False, blank=False, verbose_name=_("Face image in base64")
    )
    vector: str = models.TextField(
        null=False, blank=False, verbose_name=_("Face base64")
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = _("Recognized face")
        verbose_name_plural = _("Recognized faces")
