from django.urls import reverse
from core.tests import IntegrationBaseTestCase
from members.serializers import MemberCreateSerializer

class MemberCreateSerializerTest(IntegrationBaseTestCase):
    serializer = MemberCreateSerializer

    @classmethod
    def setUpTestData(cls) -> None:
        pass

    # 1st query: unique phone number check
    # 2nd query: insert new member
    
    def test_success(self):
        instance = self.serializer_test(
            expectedQueryCount=2,
            serializer=self.serializer,
            expectedResult=True,
            phone="01050175933",
            password="5933",
            password2="5933",
        )
        self.assertEqual(instance.phone, "01050175933")

    def test_mismatch_password(self):
        instance = self.serializer_test(
            expectedQueryCount=1,
            serializer=self.serializer,
            expectedResult=False,
            phone="01050175933",
            password="5933",
            password2="59332",
        )

    def test_empty_phone(self):
        instance = self.serializer_test(
            expectedQueryCount=0,
            serializer=self.serializer,
            expectedResult=False,
            phone="",
            password="5933",
            password2="59333",
        )

    def test_register_repeated_phone(self):
        instance = self.serializer_test(
            serializer=self.serializer,
            expectedResult=True,
            phone="01050175933",
            password="5933",
            password2="5933",
        )
        instance = self.serializer_test(
            expectedQueryCount=1,
            serializer=self.serializer,
            expectedResult=False,
            phone="01050175933",
            password="5933",
            password2="5933",
        )