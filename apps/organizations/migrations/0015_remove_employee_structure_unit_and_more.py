# Generated by Django 5.0.3 on 2024-03-31 19:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0014_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='structure_unit',
        ),
        migrations.AddField(
            model_name='structureunit',
            name='department_members',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.employeeposition'),
        ),
    ]
