# Generated by Django 5.0.3 on 2024-03-31 18:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='application',
            name='employee',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='application', to='organizations.employee', verbose_name='Employee'),
        ),
        migrations.AddField(
            model_name='employeeevent',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='organizations.employee', verbose_name='Employee'),
        ),
        migrations.AddField(
            model_name='employeeposition',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='organizations.employee', verbose_name='Employee'),
        ),
        migrations.AddField(
            model_name='organization',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='organizations.organization', verbose_name='Parent'),
        ),
        migrations.AddField(
            model_name='employee',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='organizations.organization', verbose_name='Organization'),
        ),
        migrations.AddField(
            model_name='structureunit',
            name='department_members',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.employeeposition', verbose_name='Employee Position'),
        ),
        migrations.AddField(
            model_name='structureunit',
            name='department_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='structure_units', to='organizations.departmentname', verbose_name='Department name'),
        ),
        migrations.AddField(
            model_name='structureunit',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='structure_units', to='organizations.organization', verbose_name='Organization'),
        ),
        migrations.AddField(
            model_name='structureunit',
            name='position_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='structure_units', to='organizations.positionname', verbose_name='Position name'),
        ),
        migrations.AddField(
            model_name='structureunit',
            name='tn_parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tn_children', to='organizations.structureunit', verbose_name='Parent'),
        ),
        migrations.AddField(
            model_name='employeeposition',
            name='work_shift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.workshift', verbose_name='Work shift'),
        ),
        migrations.AddField(
            model_name='employee',
            name='work_shift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='work_shift', to='organizations.workshift', verbose_name='Work shift'),
        ),
    ]
