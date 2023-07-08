from django.test import TestCase
from typing import Optional, Dict
from django.core.serializers.base import Serializer

# e2e tests
from members.models import Member
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# common
from django.db import connection, reset_queries
from django.test import TestCase, override_settings


def wrapFunctionForQueryCount(count):
    def decorator(func):
        @override_settings(DEBUG=True)
        def wrapper(*args, **kwargs):
            reset_queries()
            ret = func(*args, **kwargs)
            queries = connection.queries
            # for query in queries:
            #     print(f"QUERY: {query['sql']}, TIME: {query['time']}")
            assert len(queries) == count, "QUERY COUNT:%d != %d" % (len(queries), count)
            return ret
        return wrapper
    return decorator

class E2EBaseTestCase(TestCase):
    def generic_test(
        self,
        url,
        method,
        expectedStatusCode,
        expectedQueryCount: Optional[int] = None,
        authMember: Optional[Member] = None,
        **data,
    ):
        request = getattr(self.client, method)

        if expectedQueryCount:
            request = wrapFunctionForQueryCount(expectedQueryCount)(request)

        header = self.getAuthHeaderByToken(self.getToken(authMember))
        response = request(
            url,
            data=data,
            format="json",
            content_type="application/json",
            **header
        )
        self.assertEqual(expectedStatusCode, response.status_code)
    

    @classmethod
    def createMember(cls, **kwargs):
        return Member.objects.createMember(**kwargs)

    def getToken(self, member):
        if not member:
            return None
        serializer = TokenObtainPairSerializer(
            data={
                "phone": member.phone,
                "password": 5933,
            }
        )
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data
    
    def getAuthHeaderByToken(self, token):
        if not token:
            return {}
        return {"HTTP_AUTHORIZATION": f'Bearer {token["access"]}'}

class TestSerializerHelper():
    def __init__(self, serializer: Serializer, queryCnt: int = 0):
        self.serializer = serializer
        self.queryCnt = queryCnt

    def _create(self, data):
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            instance = serializer.create(data)
            return instance
        else:
            serializer.is_valid(raise_exception=True)
    
    def create(self, data):
        createData = self._create
        if self.queryCnt:
            createData = wrapFunctionForQueryCount(self.queryCnt)(self._create)
        return createData(data)
    
    def run(self, data: Optional[Dict]):
        if self.serializer.serializer_type == "create":
            return self.create(data)

class IntegrationSerializerTestCase(TestCase):
    def serializer_test(
        self,
        expectedQueryCount: Optional[int] = None,
        expectedResult: Optional[bool] = None,
        **data,
    ):
        testSerializerHelper = TestSerializerHelper(self.serializer, expectedQueryCount)

        instance = None
        try:
            instance = testSerializerHelper.run(data)
            self.assertEqual(expectedResult, True)
        except Exception as e:
            self.assertEqual(expectedResult, False)
        return instance