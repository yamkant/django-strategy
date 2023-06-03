from django.contrib.auth.models import User
from django.http import HttpResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema_view
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers, status
from spectacular_example.serializers import CustomUserSerializer, UserSerializer
from spectacular_example.schemas import USER_QUERY_PARAM_USERNAME_EXAMPLES, USER_QUERY_PARAM_DATE_JOINED_EXAMPLES, USER_CREATE_EXAMPLES

# Create your views here.
@extend_schema_view(
    # list method에 한하여 아래 파라미터들 지정
    list=extend_schema(
        summary="사용자들 리스트를 조회합니다.",
        tags=["사용자"],
        parameters=[
            OpenApiParameter(
                name="username",
                description="Filter by username",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                examples= USER_QUERY_PARAM_USERNAME_EXAMPLES
            ),
            OpenApiParameter(
                name="date_joined",
                description="Filter by release date",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                examples= USER_QUERY_PARAM_DATE_JOINED_EXAMPLES
            ),
        ],
    ),
    custom_api=extend_schema(
        summary="@action 데코레이터로 생성한 커스텀 API",
        tags=["사용자"],
        request=UserSerializer,
        responses={status.HTTP_200_OK: UserSerializer},
    ),
)
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        tags=["사용자"],
        summary="새로운 사용자를 추가합니다.",
        examples = USER_CREATE_EXAMPLES,
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        response: HttpResponse = super().create(request, *args, **kwargs)
        return response

    @action(detail=False, url_path="action-api")
    def custom_api(self, request: Request, *args, **kwargs):
        return Response(data={"result": "ok"})