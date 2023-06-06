from django.urls import reverse
from core.tests import IntegrationBaseTestCase
from members.serializers import MemberCreateSerializer

class MemberCreateSerializerTest(IntegrationBaseTestCase):
    serializer = MemberCreateSerializer

    @classmethod
    def setUpTestData(cls) -> None:
        pass
    
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
            expectedQueryCount=2,
            serializer=self.serializer,
            expectedResult=False,
            phone="01050175933",
            password="5933",
            password2="59332",
        )

    def test_empty_phone(self):
        instance = self.serializer_test(
            expectedQueryCount=2,
            serializer=self.serializer,
            expectedResult=False,
            phone="",
            password="5933",
            password2="59333",
        )