# Generated by Django 5.0.2 on 2024-03-30 07:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DepartmentName",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
            ],
            options={
                "verbose_name": "Department name",
                "verbose_name_plural": "Department names",
            },
        ),
        migrations.CreateModel(
            name="PositionName",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="WorkShift",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("schedule", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_developer", models.BooleanField(default=False)),
                ("active_from", models.DateField(verbose_name="Active from")),
                (
                    "active_to",
                    models.DateField(blank=True, null=True, verbose_name="Active to"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                ("bin", models.CharField(max_length=12, verbose_name="BIN")),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="main.organization",
                        verbose_name="Parent",
                    ),
                ),
            ],
            options={
                "verbose_name": "Organization",
                "verbose_name_plural": "Organizations",
            },
        ),
        migrations.CreateModel(
            name="EmployeePosition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.employee",
                        verbose_name="Сотрудник",
                    ),
                ),
                (
                    "position",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.positionname",
                        verbose_name="Позиция сотрудника",
                    ),
                ),
                (
                    "work_shift",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.workshift",
                        verbose_name="Смена сотрудника",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StructureUnit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("organization", "Организация"),
                            ("department", "Отдел"),
                            ("division", "Подразделение"),
                            ("section", "Секция"),
                            ("branch", "Филиал"),
                            ("office", "Офис"),
                            ("position", "Должность"),
                            ("other", "Другое"),
                        ],
                        default="department",
                        max_length=20,
                        verbose_name="Type",
                    ),
                ),
                (
                    "is_department_leader",
                    models.BooleanField(
                        default=False, verbose_name="Is department leader"
                    ),
                ),
                (
                    "department_leader",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.employeeposition",
                    ),
                ),
                (
                    "department_name",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="structure_units",
                        to="main.departmentname",
                        verbose_name="Department name",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="structure_units",
                        to="main.organization",
                        verbose_name="Organization",
                    ),
                ),
                (
                    "position_name",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="structure_units",
                        to="main.positionname",
                        verbose_name="Position name",
                    ),
                ),
            ],
            options={
                "verbose_name": "Structure unit",
                "verbose_name_plural": "Structure units",
            },
        ),
    ]