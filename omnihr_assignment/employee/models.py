from django.db import models
from omnihr_assignment.users.models import Company


class Employee(models.Model):
    class EmployeeStatusChoice(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        NOT_STARTED = 'Not started', 'Not started'
        TERMINATED = 'Terminated', 'Terminated'

    first_name = models.CharField(null=True, blank=True, max_length=255)
    last_name = models.CharField(null=True, blank=True, max_length=255)
    phone_number = models.CharField(null=True, blank=True, max_length=20)
    email = models.EmailField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True,
                                 choices=EmployeeStatusChoice.choices, default=EmployeeStatusChoice.ACTIVE)
    department = models.ForeignKey('Department', related_name='employee_department', null=True, on_delete=models.SET_NULL)
    position = models.ForeignKey('Position', related_name='employee_position', null=True, on_delete=models.SET_NULL)
    location = models.ForeignKey('Location', related_name='employee_location', null=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(Company, related_name='employee_company', null=True, on_delete=models.SET_NULL)

class Department(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    description = models.CharField(null=True, blank=True, max_length=255)


class Position(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    description = models.CharField(null=True, blank=True, max_length=255)


class Location(models.Model):
    country = models.CharField(null=True, blank=True, max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longtitude = models.FloatField(null=True, blank=True)
    zip_code = models.CharField(null=True, blank=True, max_length=15)