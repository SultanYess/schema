# Generated by Django 5.0.3 on 2024-03-31 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0012_remove_employee_structure_unit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='structureunit',
            name='department_name',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='work_shift',
        ),
        migrations.RemoveField(
            model_name='employeeposition',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='employeeevent',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='structureunit',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='structureunit',
            name='position_name',
        ),
        migrations.RemoveField(
            model_name='structureunit',
            name='tn_parent',
        ),
        migrations.DeleteModel(
            name='Application',
        ),
        migrations.DeleteModel(
            name='DepartmentName',
        ),
        migrations.DeleteModel(
            name='WorkShift',
        ),
        migrations.DeleteModel(
            name='EmployeePosition',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.DeleteModel(
            name='EmployeeEvent',
        ),
        migrations.DeleteModel(
            name='Organization',
        ),
        migrations.DeleteModel(
            name='PositionName',
        ),
        migrations.DeleteModel(
            name='StructureUnit',
        ),
    ]
