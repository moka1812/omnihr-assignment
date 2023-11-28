from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from omnihr_assignment.employee.models import Employee


class EmployeeSerializer(ModelSerializer):
    department = serializers.ReadOnlyField(source='department.name')
    company = serializers.ReadOnlyField(source='company.name')
    location = serializers.ReadOnlyField(source='location.country')
    position = serializers.ReadOnlyField(source='position.name')

    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        default_fields = ["id", "status", "first_name", "last_name"]

        if fields is not None and fields == []:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed - default_fields:
                self.fields.pop(field_name)