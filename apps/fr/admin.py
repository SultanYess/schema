from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _


from apps.common.mixins import admin as mixin_admin
from apps.fr.models import OriginalImage, RecognizedFace


class RecognizedFaceInline(mixin_admin.ReadOnlyModelAdmin, admin.StackedInline):
    model = RecognizedFace
    extra = 0
    show_change_link = True


@admin.register(OriginalImage)
class OriginalImageAdmin(mixin_admin.ReadOnlyModelAdmin, admin.ModelAdmin):
    list_display = (
        "created_at",
        "created_by",
    )
    list_filter = ("created_at",)
    search_fields = (
        "created_by__username",
        "created_by__last_name",
        "created_by__first_name",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "created_at",
                    "created_by",
                    "image_tag",
                )
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("-created_at")

    inlines = (RecognizedFaceInline,)

    def image_tag(self, obj):
        return mark_safe(
            f'<img src="{obj.original_image.url}" style="max-height:250px; height: auto;" class="rounded" />'
        )

    image_tag.short_description = _("Image")


@admin.register(RecognizedFace)
class RecognizedFaceAdmin(mixin_admin.ReadOnlyModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
    )
    fieldsets = (
        (
            None,
            {"fields": ("id", "face_image_tag", "original_image", "vector")},
        ),
    )

    def face_image_tag(self, obj):
        return mark_safe(
            f'<img src="data:image/jpeg;base64,{obj.face_image}" style="max-height:250px; height: auto;" class="rounded" />'
        )

    face_image_tag.short_description = _("Image")
