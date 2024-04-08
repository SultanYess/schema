# Generated by Django 5.0.3 on 2024-04-01 06:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0015_remove_employee_structure_unit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='structureunit',
            name='department_members',
        ),
        migrations.AddField(
            model_name='employee',
            name='structure_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.structureunit', verbose_name='Structure unit'),
        ),
        migrations.AddField(
            model_name='employeeposition',
            name='structure_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.structureunit', verbose_name='Structure unit'),
        ),
    ]
