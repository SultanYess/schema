from django.db import models
from django.contrib.auth.models import User
import datetime
from .import *
from django.db.models import ForeignKey


class PositionName(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.name


class Organization(models.Model):
    """Организации"""

    name: str = models.CharField(max_length=255, verbose_name="Name")
    description: str = models.TextField(
        null=True, blank=True, verbose_name="Description"
    )
    bin: str = models.CharField(max_length=12, verbose_name="BIN")
    parent: "Organization" = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Parent",
    )

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return f"{self.name}"


class DepartmentName(models.Model):
    """Наименования подразделений"""

    name: str = models.CharField(max_length=255, verbose_name="Name")
    description: str = models.TextField(
        null=True, blank=True, verbose_name="Description"
    )

    class Meta:
        verbose_name = "Department name"
        verbose_name_plural ="Department names"

    def __str__(self):
        return f"{self.name}"

class WorkShift(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    schedule = models.CharField(max_length=255, verbose_name="Schedule")

    def __str__(self):
        return f"{self.name}"


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_developer = models.BooleanField(default=False)
    active_from: datetime.date = models.DateField(verbose_name="Active from")
    active_to: datetime.date = models.DateField(
        null=True, blank=True, verbose_name="Active to"
    )

    def __str__(self):
        return f"{self.user}"


class EmployeePosition(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
    position = ForeignKey(PositionName, on_delete=models.CASCADE, verbose_name='Позиция сотрудника')
    # work_shift = ForeignKey(WorkShift, on_delete=models.CASCADE, verbose_name='Смена сотрудника')

    def __str__(self):
        return f"{self.employee} / {self.position}"


class EmployeeWorkShift(models.Model):
    employee = ForeignKey(EmployeePosition, on_delete=models.CASCADE, verbose_name='Employee')
    work_shift = ForeignKey(WorkShift, on_delete=models.CASCADE, verbose_name='Work_Shift')

class StructureUnit(models.Model):
    type: str = models.CharField(
        max_length=20,
        choices=StructureUnitTypes.choices,
        null=False,
        blank=False,
        default=StructureUnitTypes.DEPARTMENT,
        verbose_name="Type",
    )

    organization: Organization = models.ForeignKey(
        Organization,
        related_name="structure_units",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Organization",
    )

    department_name: DepartmentName = models.ForeignKey(
        DepartmentName,
        related_name="structure_units",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Department name",
    )

    position_name: PositionName = models.ForeignKey(
        PositionName,
        related_name="structure_units",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Position name",
    )

    department_members = ForeignKey(EmployeePosition, on_delete=models.CASCADE, null=True, blank=True)
    is_department_leader: bool = models.BooleanField(
        default=False, verbose_name="Is department leader"
    )

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

        verbose_name = "Structure unit"
        verbose_name_plural = "Structure units"

    def __str__(self):
        return f"{self.name}"


class ChangeTimeRequest(models.Model):
    employee: Employee = models.ForeignKey(
        Employee,
        related_name="application",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Employee",
        default="",
    )
    date = models.DateTimeField(null=False, blank=False, verbose_name="Event date")
    type: str = models.CharField(
        max_length=100,
        choices=EmployeeEventTypes.choices,
        null=False,
        blank=False,
        verbose_name="Event type",
    )
    comment: str = models.TextField(verbose_name="Comment")
    change_status: str = models.CharField(
        max_length=100,
        choices=ChangeTimeRequestTypes.choices,
        null=False,
        blank=False,
        verbose_name="Event type",
    )