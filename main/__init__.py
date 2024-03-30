from django.db import models


class StructureUnitTypes(models.TextChoices):
    """Типы структурных подразделений"""

    ORGANIZATION = "organization", "Организация"
    DEPARTMENT = "department", "Отдел"
    DIVISION = "division", "Подразделение"
    SECTION = "section", "Секция"
    BRANCH = "branch", "Филиал"
    OFFICE = "office", "Офис"
    POSITION = "position", "Должность"
    OTHER = "other", "Другое"


class EmploymentTypes(models.TextChoices):
    """Типы занятости"""

    FULL_TIME = "full_time", "Полная занятость"
    PART_TIME = "part_time", "Частичная занятость"
    PROJECT = "project", "Проектная работа"
    INTERNSHIP = "internship", "Стажировка"
    VOLUNTEERING = "volunteering", "Волонтерство"
    CIVIL_CONTRACT = "civil_contract", "Договор гражданско-правового характера"
    OTHER = "other", "Другое"


class WorkScheduleTypes(models.TextChoices):
    """Типы графиков работы"""

    FULL_DAY = "full_day", "Полный день"
    SHIFT = "shift", "Сменный график"
    FLEXIBLE = "flexible", "Гибкий график"
    REMOTE = "remote", "Удаленная работа"
    FLY_IN_FLY_OUT = "fly_in_fly_out", "Вахтовый метод"
    ROTATION = "rotation", "Ротация"
    OTHER = "other", "Другое"


class EmployeeEventTypes(models.TextChoices):
    """Типы событий сотрудников"""

    DAY_OFF = "day_off", "Отгул"
    VACATION = "vacation", "Отпуск"
    SICK_LEAVE = "sick_leave", "Больничный"
    BUSINESS_TRIP = "business_trip", "Командировка"
    COMING = "coming", "Прибытие"
    LEAVING = "leaving", "Убытие"
    COMING_HR = "coming_hr", "Прибытие [HR]"
    LEAVING_HR = "leaving_hr", "Убытие [HR]"
    OTHER = "other", "Другое"


class ChangeTimeRequestTypes(models.TextChoices):
    IN_PROCESS = "in_process", "В процессе"
    CONFIRMED = "confirmed", "Принято"
    CANCELED = "canceled", "Отменено"