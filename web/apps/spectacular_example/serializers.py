from django.contrib.auth.models import User
from rest_framework import serializers, status
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework.serializers import ModelSerializer

@extend_schema_serializer(
    exclude_fields=("password",),  
    examples=[
        OpenApiExample(
            "Valid example 1",
            summary="short summary",
            description="longer description",
            value={
                "is_superuser": True,
                "username": "string",
                "first_name": "string",
                "last_name": "string",
                "email": "user@example.com",
                "is_staff": False,
                "is_active": True,
                "date_joined": "2021-04-18 04:14:30",
                "user_type": "customer",
            },
            request_only=True,
            response_only=False,  
        ),
    ],
)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        depth = 1
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(help_text="회원의 유형값을 받습니다.", default="customer")

    class Meta:
        model = User
        fields = "__all__"