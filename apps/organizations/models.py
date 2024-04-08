import datetime as dt
import uuid as _uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from treenode.models import TreeNodeModel

from apps.common.mixins import models as mixin_models
from apps.organizations import (
    EmploymentTypes,
    StructureUnitTypes,
    WorkScheduleTypes,
    EmployeeEventTypes,
)
from apps.fr.models import RecognizedFace
User = get_user_model()


class Organization(mixin_models.TimestampModel):
    """Организации"""

    id: _uuid.UUID = models.UUIDField(
        primary_key=True,
        default=_uuid.uuid4,
        unique=True,
        editable=False,
        name="id",
        verbose_name=_("UUID identification"),
    )

    name: str = models.CharField(max_length=255, verbose_name=_("Name"))
    description: str = models.TextField(
        null=True, blank=True, verbose_name=_("Description")
    )
    bin: str = models.CharField(max_length=12, verbose_name=_("BIN"))
    parent_id: _uuid.UUID
    parent: "Organization" = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Parent"),
    )

    class Meta:
        ordering = [
            "-created_at",
        ]
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __str__(self):
        return f"{self.name}"


class DepartmentName(mixin_models.TimestampModel):
    """Наименования подразделений"""

    id: _uuid.UUID = models.UUIDField(
        primary_key=True,
        default=_uuid.uuid4,
        unique=True,
        editable=False,
        name="id",
        verbose_name=_("UUID identification"),
    )

    name: str = models.CharField(max_length=255, verbose_name=_("Name"))
    description: str = models.TextField(
        null=True, blank=True, verbose_name=_("Description")
    )

    class Meta:
        ordering = [
            "-created_at",
        ]
        verbose_name = _("Department name")
        verbose_name_plural = _("Department names")

    def __str__(self):
        return f"{self.name}"


class PositionName(mixin_models.TimestampModel):
    """Наименования должностей"""

    id: _uuid.UUID = models.UUIDField(
        primary_key=True,
        default=_uuid.uuid4,
        unique=True,
        editable=False,
        name="id",
        verbose_name=_("UUID identification"),
    )
    name: str = models.CharField(max_length=255, verbose_name=_("Name"))
    description: str = models.TextField(
        null=True, blank=True, verbose_name=_("Description")
    )

    class Meta:
        ordering = [
            "-created_at",
        ]
        verbose_name = _("Position name")
        verbose_name_plural = _("Position names")

    def __str__(self):
        return f"{self.name}"


class StructureUnit(mixin_models.TimestampModel, mixin_models.UUIDModel, TreeNodeModel):
    """Структурные подразделения"""

    id: _uuid.UUID = models.UUIDField(
        primary_key=True,
        default=_uuid.uuid4,
        unique=True,
        editable=False,
        name="id",
        verbose_name=_("UUID identification"),
    )

    type: str = models.CharField(
        max_length=20,
        choices=StructureUnitTypes.choices,
        null=False,
        blank=False,
        default=StructureUnitTypes.DEPARTMENT,
        verbose_name=_("Type"),
    )

    organization_id: _uuid.UUID
    organization: Organization = models.ForeignKey(
        Organization,
        related_name="structure_units",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Organization"),
    )

    department_name_id: _uuid.UUID
    department_name: DepartmentName = models.ForeignKey(
        DepartmentName,
        related_name="structure_units",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Department name"),
    )

    position_name_id: _uuid.UUID
    position_name: PositionName = models.ForeignKey(
        PositionName,
        related_name="structure_units",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Position name"),
    )

    is_department_leader: bool = models.BooleanField(
        default=False, verbose_name=_("Is department leader")
    )

    treenode_display_field = "name"

    @property
    def name(self):
        if self.type == StructureUnitTypes.POSITION:
            return f"{self.position_name}"
        if self.type == StructureUnitTypes.ORGANIZATION:
            return f"{self.organization}"
        return self.department_name

    def get_full_name(self):
        if self.parent:
            return f"{self.parent.get_full_name()} / {self.name}"
        return self.name

    def get_organization(self):
        if self.organization:
            return self.organization
        if self.parent:
            return self.parent.get_organization()
        return None

    class Meta:
        ordering = [
            "-created_at",
        ]
        verbose_name = _("Structure unit")
        verbose_name_plural = _("Structure units")

    def __str__(self):
        return f"{self.name}"


class WorkShift(mixin_models.TimestampModel):
    id: _uuid.UUID = models.UUIDField(
        primary_key=True,
        default=_uuid.uuid4,
        unique=True,
        editable=False,
        name="id",
        verbose_name=_("UUID identification"),
    )
    name: str = models.CharField(max_length=255, verbose_name=_("Shift Name"))
    schedule: str = models.CharField(max_length=100, verbose_name=_("Shift Schedule"))

    def __str__(self):
        return f"{self.name}"


class Employee(mixin_models.TimestampModel):
    """Сотрудники"""

    id: _uuid.UUID = models.UUIDField(
        primary_key=True,
        default=_uuid.uuid4,
        unique=True,
        editable=False,
        name="id",
        verbose_name=_("UUID identification"),
    )

    organization_id: _uuid.UUID
    organization: Organization = models.ForeignKey(
        Organization,
        related_name="employees",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("Organization"),
    )

    user_id: _uuid.UUID
    user: User = models.ForeignKey(
        User,
        related_name="employees",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("User"),
    )
    employment_type: str = models.CharField(
        max_length=20,
        choices=EmploymentTypes.choices,
        null=False,
        blank=False,
        default=EmploymentTypes.FULL_TIME,
        verbose_name=_("Employment type"),
    )
    structure_unit: StructureUnit = models.ForeignKey(
        StructureUnit,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Structure unit")
    )
    active_from: dt.date = models.DateField(verbose_name=_("Active from"))
    active_to: dt.date = models.DateField(
        null=True, blank=True, verbose_name=_("Active to")
    )

    class Meta:
        ordering = [
            "-created_at",
        ]
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return f"{self.user} [{self.organization}]"


class EmployeePosition(mixin_models.TimestampModel):
    """Должности сотрудников"""

    id: _uuid.UUID = models.UUIDField(
        primary_key=True,
        default=_uuid.uuid4,
        unique=True,
        editable=False,
        name="id",
        verbose_name=_("UUID identification"),
    )

    employee_id: _uuid.UUID
    employee: Employee = models.ForeignKey(
        Employee,
        related_name="positions",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("Employee"),
    )

    structure_unit_id: _uuid.UUID
    structure_unit: StructureUnit = models.ForeignKey(
        StructureUnit,
        related_name="employees",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Structure unit"),
    )
    work_schedule_type: str = models.CharField(
        max_length=20,
        choices=WorkScheduleTypes.choices,
        null=False,
        blank=False,
        default=WorkScheduleTypes.FULL_DAY,
        verbose_name=_("Work schedule type"),
    )
    work_shift_id: _uuid.UUID
    work_shift: WorkShift = models.ForeignKey(
        WorkShift,
        on_delete=models.CASCADE,
        verbose_name=_("Work Shift"),
        null=True,
        blank=True
    )

    active_from: dt.date = models.DateField(verbose_name=_("Active from"))
    active_to: dt.date = models.DateField(
        null=True, blank=True, verbose_name=_("Active to")
    )

    class Meta:
        ordering = [
            "-created_at",
        ]
        verbose_name = _("Employee position")
        verbose_name_plural = _("Employee positions")

    def __str__(self):
        return f"{self.employee} {self.structure_unit} [{self.active_from} - {self.active_to}]"


class EmployeeEvent(mixin_models.TimestampModel):
    """События сотрудников"""

    id: _uuid.UUID = models.UUIDField(
        primary_key=True,
        default=_uuid.uuid4,
        unique=True,
        editable=False,
        name="id",
        verbose_name=_("UUID identification"),
    )

    employee_id: _uuid.UUID
    employee: Employee = models.ForeignKey(
        Employee,
        related_name="events",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("Employee"),
    )

    event_type: str = models.CharField(
        max_length=100,
        choices=EmployeeEventTypes.choices,
        null=False,
        blank=False,
        verbose_name=_("Event type"),
    )
    event_start_date: dt.date = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Event start date")
    )
    event_note: str = models.TextField(
        null=True, blank=True, verbose_name=_("Event note")
    )

    class Meta:
        ordering = [
            "-created_at",
        ]
        verbose_name = _("Employee event")
        verbose_name_plural = _("Employee events")

    def __str__(self):
        return f"{self.employee} {self.event_type} {self.event_start_date}"


APPLICATION_STATUS = {
    "for_consideration": " На рассмотрений",
    "approved": "Одобрено",
    "canceled": "Отменено",
}


class Application(mixin_models.TimestampModel):
    id: _uuid.UUID = models.UUIDField(
        primary_key=True,
        default=_uuid.uuid4,
        unique=True,
        editable=False,
        name="id",
        verbose_name=_("UUID identification"),
    )
    employee: Employee = models.ForeignKey(
        Employee,
        related_name="application",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("Employee"),
        default="",
    )
    date = models.DateTimeField(null=False, blank=False, verbose_name=_("Event date"))
    type: str = models.CharField(
        max_length=100,
        choices=EmployeeEventTypes.choices,
        null=False,
        blank=False,
        verbose_name=_("Event type"),
    )
    comment: str = models.TextField(verbose_name=_("Comment"))
    application_status = models.CharField(
        max_length=100,
        choices=APPLICATION_STATUS,
        default=APPLICATION_STATUS["for_consideration"],
        verbose_name=_("Status"),
    )

    def __str__(self):
        return f"{self.employee}"


class Event(mixin_models.TimestampModel):
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
    employee: Employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name=_("Employee"),
        null=True,
        blank=True,
    )
    recognized_face: RecognizedFace = models.ForeignKey(
        RecognizedFace,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Recognized"),
    )
    employee_event: EmployeeEvent = models.ForeignKey(
        EmployeeEvent, on_delete=models.CASCADE, verbose_name=_("Employee event")
    )

    def __str__(self):
        return f"{self.employee_event} {self.employee_event}"