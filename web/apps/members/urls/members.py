from django.urls import path
from members.views import MemberCreateAPIView, MemberLoginCheckAPIView

app_name = "members"

urlpatterns = [
    path("", MemberCreateAPIView.as_view(), name="create"),
    path("login_check", MemberLoginCheckAPIView.as_view(), name="login_check"),
]
