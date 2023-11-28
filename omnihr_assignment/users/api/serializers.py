from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from omnihr_assignment.users.models import User as UserType
from omnihr_assignment.users.models import Company


User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        refresh = self.get_token(user)
        
        
        if user.is_active is False:
            raise serializers.ValidationError({"errors": "USER_INACTIVE"})

        data['refresh'] = str(refresh)  
        data['access'] = str(refresh.access_token)
        return data