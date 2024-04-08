import datetime as dt
import re
from apps.organizations.models import *
from apps.common.mixins import admin as mixin_admin

from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Q


from treenode.admin import TreeNodeModelAdmin
from treenode.forms import TreeNodeForm


class OrganizationInline(mixin_admin.ReadOnlyModelAdmin, admin.TabularInline):
    model = Organization
    extra = 0
    show_change_link = True


class EmployeeInline(mixin_admin.ReadOnlyModelAdmin, admin.TabularInline):
    model = Employee
    extra = 0
    show_change_link = True
    fields = ("user", "active_from")


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    inlines = (OrganizationInline, EmployeeInline)
    search_fields = ("name",)


@admin.register(DepartmentName)
class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(PositionName)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class StructureUnitInline(mixin_admin.ReadOnlyModelAdmin, admin.TabularInline):
    model = StructureUnit
    extra = 0
    show_change_link = True


class EmployeePositionInline(admin.TabularInline):
    model = EmployeePosition
    extra = 0
    show_change_link = True
    autocomplete_fields = [
        "employee",
    ]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "employee":
            parent_id = request.resolver_match.kwargs.get("object_id")
            if parent_id:
                organization = StructureUnit.objects.get(
                    id=parent_id
                ).get_organization()
                if organization:
                    kwargs["queryset"] = Employee.objects.filter(
                        organization=organization
                    )
                else:
                    kwargs["queryset"] = Employee.objects.none()
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(StructureUnit)
class StructureUnitAdmin(TreeNodeModelAdmin):
    list_display = (
        "colored_type",
        "current_employee",
    )
    list_filter = ("type",)
    autocomplete_fields = (
        "organization",
        "department_name",
        "position_name",
        "tn_parent",
    )
    search_fields = (
        "department_name__name",
        "position_name__name",
        "organization__name",
    )

    treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
    form = TreeNodeForm

    def get_inlines(self, request, obj):
        if obj and obj.type == StructureUnitTypes.POSITION:
            return (
                StructureUnitInline,
                EmployeePositionInline,
            )
        return (StructureUnitInline,)

    def name(self, obj):
        return obj.name

    name.short_description = _("Name")

    def colored_type(self, obj):
        if obj.type == StructureUnitTypes.POSITION:
            is_department_leader_mark = (
                '<img src="/static/admin/img/icon-yes.svg" alt="True">'
                if obj.is_department_leader
                else ""
            )
            return format_html(
                f'<span style="color: green;">{obj.get_type_display()} {is_department_leader_mark}</span>'
            )
        if obj.type == StructureUnitTypes.ORGANIZATION:
            return format_html(
                f'<span style="color: blue;">{obj.get_type_display()}</span>'
            )
        return obj.get_type_display()

    colored_type.short_description = _("Type")

    def current_employee(self, obj):
        employees = obj.employees.filter(
            Q(active_to__gte=dt.datetime.now()) | Q(active_to__isnull=True),
            active_from__lte=dt.datetime.now(),
        )
        return ", ".join(
            [str(employee.employee.user) for employee in employees]
        )

    current_employee.short_description = _("Current employee")



@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "organization",
        "employment_type",
        "active_from",
        "active_to",
    ]
    search_fields = [
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    ]

    @staticmethod
    def get_structure_unit_id(url):
        pattern = re.compile(
            r"^.*?/admin/organizations/structureunit/(?P<uuid>[0-9a-f-]+)/change/$"
        )
        match = pattern.match(url)
        if match:
            return match.group("uuid")
        return False

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if request.path == "/admin/autocomplete/":
            header = request.META.get("HTTP_REFERER")
            if structure_unit_id := self.get_structure_unit_id(header):
                organization = StructureUnit.objects.get(
                    id=structure_unit_id
                ).get_organization()
                if organization:
                    queryset = queryset.filter(organization=organization)
                else:
                    queryset = queryset.none()
                return queryset, use_distinct

        return queryset, use_distinct


@admin.register(EmployeePosition)
class EmployeePositionAdmin(admin.ModelAdmin):
    list_display = [
        "employee",
        "structure_unit_full_name",
        "work_schedule_type",
        "active_from",
        "active_to",
    ]

    def structure_unit_full_name(self, obj):
        if obj.structure_unit:
            return obj.structure_unit.get_full_name()
        return None

    structure_unit_full_name.short_description = _("Structure Unit full name")


@admin.register(EmployeeEvent)
class EmployeeEventAdmin(admin.ModelAdmin):
    list_display = ["employee", "event_type", "event_start_date", "event_note"]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["employee", "date", "type", "comment", "application_status"]
    ordering = ["-date"]


@admin.register(WorkShift)
class WorkShiftAdmin(admin.ModelAdmin):
    list_display = ["name", "schedule"]
    ordering = ["-created_at"]

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["recognized_face", "employee_event"]
    ordering = ["-created_at"]
