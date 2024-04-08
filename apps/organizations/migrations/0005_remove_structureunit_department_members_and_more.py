# Generated by Django 5.0.3 on 2024-03-31 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_structureunit_department_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='structureunit',
            name='department_members',
        ),
        migrations.AddField(
            model_name='structureunit',
            name='department_members',
            field=models.ManyToManyField(blank=True, null=True, to='organizations.employee', verbose_name='Department Members'),
        ),
    ]
