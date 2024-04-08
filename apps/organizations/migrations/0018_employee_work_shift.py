# Generated by Django 5.0.3 on 2024-04-01 07:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0017_rename_employee_type_employee_employment_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='work_shift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.workshift', verbose_name='Work Shift'),
        ),
    ]
