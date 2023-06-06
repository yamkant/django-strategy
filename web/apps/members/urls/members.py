from django.urls import path
from members.views import MemberCreateAPIView

app_name = "members"

urlpatterns = [
    path("", MemberCreateAPIView.as_view(), name="create"),
]
