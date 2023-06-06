from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt import views as jwt_views

from members.serializers import (
    MemberCreateSerializer,
)

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema_view
from drf_spectacular.utils import extend_schema
from members.serializers import MemberCreateSerializer
# from spectacular_example.schemas import USER_QUERY_PARAM_USERNAME_EXAMPLES, USER_QUERY_PARAM_DATE_JOINED_EXAMPLES, USER_CREATE_EXAMPLES

@extend_schema(
    tags=["사용자"],
    summary="새로운 사용자를 추가합니다.",
    # examples = USER_CREATE_EXAMPLES,
)
class MemberCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = MemberCreateSerializer

@extend_schema(
    tags=["사용자"],
    summary="로그인 여부를 체크합니다.",
    # examples = USER_CREATE_EXAMPLES,
)
class MemberLoginCheckAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "This user is logged in."}, status=status.HTTP_200_OK)


class TokenCreateAPIView(jwt_views.TokenObtainPairView):
    pass

class TokenRefreshAPIView(jwt_views.TokenRefreshView):
    pass
    
class TokenBlackListAPIView(jwt_views.TokenBlacklistView):
    pass