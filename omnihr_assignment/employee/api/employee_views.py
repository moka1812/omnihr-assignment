from rest_framework import generics
from rest_framework import permissions
from omnihr_assignment.employee.models import Employee
from omnihr_assignment.utils.paginations import CustomPagination
from omnihr_assignment.employee.api.employee_serializers import EmployeeSerializer
from omnihr_assignment.utils.processing import _dumps_dict_for_hash_map
from omnihr_assignment.permission.rate_limit import RateLimitPermission
from django.conf import settings

import redis, json


redisClient = redis.StrictRedis(host=settings.REDIS_HOST,port=6379,db=0)


class EmployeeListView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = (permissions.IsAuthenticated, RateLimitPermission)

    def get_queryset(self):        
        qs = self.queryset
        status = self.request.query_params.get('status')
        if status is not None:
            print(status.split(','))
            qs = qs.filter(status__in=status.split(','))

        location = self.request.query_params.get('location')
        if location is not None:       
            qs = qs.filter(location=location)

        department = self.request.query_params.get('department')
        if department is not None:       
            qs = qs.filter(department=department)
            
        position = self.request.query_params.get('position')
        if position is not None:       
            qs = qs.filter(position=position)

        return qs
    
    def list(self, request, *args, **kwargs):
        paginator = CustomPagination()
        user = self.request.user
        qs = self.get_queryset()
        # Get dynamic field config by company id
        dynamic_fields_key =  "EMPLOYEE_FIELDS"
        fields = redisClient.hget(name=dynamic_fields_key, key=user.company.id).decode('utf-8')
        fields = json.loads(fields)            

        page = paginator.paginate_queryset(qs.filter(company=user.company), request)
        serializer = self.serializer_class(page, fields=fields, many=True)
        return paginator.get_paginated_response(serializer.data)