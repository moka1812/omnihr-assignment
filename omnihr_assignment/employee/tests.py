from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from omnihr_assignment.users.models import Company
from omnihr_assignment.employee.models import Employee, Location, Position, Department
from omnihr_assignment.employee.api.employee_serializers import EmployeeSerializer

User = get_user_model()

class EmployeeListTest(APITestCase):
    def test_get_all_employee(self):
        # Get token auth
        company = Company.objects.create(name='Test')
        user = User.objects.create_user(email='quang@test.io', password='test', company=company)
        # Setup data
        location = Location.objects.create(country='Singapore')
        position = Position.objects.create(name='Backend Developer')
        department = Department.objects.create(name='Technical')

        Employee.objects.create(first_name='Quang', last_name='Tran', location=location, position=position, department=department, company=company)

        refresh = RefreshToken.for_user(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Test happy case
        response = client.get(reverse('list-employee'))
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"], serializer.data)

        # Cannot get data from other company
        new_company = Company.objects.create(name='Test2')
        Employee.objects.create(first_name='Quang2', last_name='Tran', location=location, position=position, department=department, company=new_company)
        response = client.get(reverse('list-employee'))
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data["data"], serializer.data)

        # Filter by status
        Employee.objects.create(first_name='Quang3', last_name='Tran', location=location, position=position, department=department, company=company, status=Employee.EmployeeStatusChoice.NOT_STARTED)
        response = client.get(reverse('list-employee'), {'status': 'Active'})
        employee = Employee.objects.filter(status='Active', company=company)
        serializer = EmployeeSerializer(employee, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"], serializer.data)

        # Filter by location
        new_location = Location.objects.create(country='Vietnam')
        Employee.objects.create(first_name='Quang4', last_name='Tran', location=new_location, position=position, department=department, company=company)
        response = client.get(reverse('list-employee'), {'location': location.id})
        employee = Employee.objects.filter(location=location, company=company)
        serializer = EmployeeSerializer(employee, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"], serializer.data)

        # Filter by position
        new_position = Position.objects.create(name='Tech Lead')
        Employee.objects.create(first_name='Quang5', last_name='Tran', location=location, position=new_position, department=department, company=company)
        response = client.get(reverse('list-employee'), {'position': position.id})
        employee = Employee.objects.filter(position=position, company=company)
        serializer = EmployeeSerializer(employee, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"], serializer.data)

        # Filter by department
        new_department = Department.objects.create(name='Accountant')
        Employee.objects.create(first_name='Quang6', last_name='Tran', location=location, position=position, department=new_department, company=company)
        response = client.get(reverse('list-employee'), {'department': department.id})
        employee = Employee.objects.filter(department=department, company=company)
        serializer = EmployeeSerializer(employee, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"], serializer.data)