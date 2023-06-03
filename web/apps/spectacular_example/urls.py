from django.urls import path
from spectacular_example.views import UserViewSet

app_name = "test_app"

user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
custom_user_list = UserViewSet.as_view({
    'get': 'custom_api',
})

urlpatterns = [
    path("", user_list),
    path("custom-action-api/", custom_user_list),
]
