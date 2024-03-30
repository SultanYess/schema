from django.contrib import admin

from .models import *

class EmployeePositionInline(admin.TabularInline):
    model = EmployeePosition
    extra = 0
    show_change_link = True
    autocomplete_fields = [
        "employee",
    ]

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_developer', 'active_from', 'active_to', )


@admin.register(EmployeePosition)
class EmployeePositionAdmin(admin.ModelAdmin):
    list_display = ('employee', 'position')

@admin.register(DepartmentName)
class DepartmentNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(StructureUnit)
class StructureUnitAdmin(admin.ModelAdmin):
    list_display = ('type', 'organization', 'department_name', 'position_name', 'department_members', 'is_department_leader')


@admin.register(WorkShift)
class WorkShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'schedule')

@admin.register(PositionName)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(EmployeeWorkShift)
class EmployeeWorkShiftAdmin(admin.ModelAdmin):
    list_display = ('employee', 'work_shift')