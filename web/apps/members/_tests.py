from django.urls import reverse
from core.tests import E2EBaseTestCase

class MemberCreateAPIViewTest(E2EBaseTestCase):
    url = reverse('members:create')

    @classmethod
    def setUpTestData(cls) -> None:
        pass
    
    def test_success(self):
        self.generic_test(
            url=self.url,
            method="post",
            expectedStatusCode=201,
            expectedQueryCount=2,
            phone="01050175933",
            password="5933",
            password2="5933",
        )

    def test_mismatch_password(self):
        self.generic_test(
            url=self.url,
            method="post",
            expectedStatusCode=400,
            phone="01050175933",
            password="5933",
            password2="59332",
        )
    
    def test_invalid_phone_number(self):
        self.generic_test(
            url=self.url,
            method="post",
            expectedStatusCode=400,
            phone="010-5017-5933",
            password="5933",
            password2="5933",
        )

class MemberLoginCheckAPIViewTest(E2EBaseTestCase): 
    url = reverse('members:login_check')

    def test_success(self):
        authMember = self.createMember(
            phone="01050175933",
            password="5933"
        )
        self.generic_test(
            url=self.url,
            method="get",
            expectedStatusCode=200,
            expectedQueryCount=0,
            authMember=authMember
        )

    def test_without_login(self):
        self.generic_test(
            url=self.url,
            method="get",
            expectedStatusCode=401,
            expectedQueryCount=0,
            authMember=None
        )
