from rest_framework.serializers import ModelSerializer
from students.models import Student
from employees.models import Employee


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
