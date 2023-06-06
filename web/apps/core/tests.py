from django.test import TestCase
from typing import Optional
from django.core.serializers.base import Serializer

# Create your tests here.
from django.test import TestCase, override_settings
from members.models import Member
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.serializers import CreateSerializer

from django.db import connection, reset_queries


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

class IntegrationBaseTestCase(TestCase):
    def serializer_test(
        self,
        expectedQueryCount: Optional[int] = None,
        serializer: Optional[Serializer] = None,
        expectedResult: Optional[bool] = None,
        **data,
    ):
        def createData(serializer, data):
            targetSerializer = serializer(data=data)
            if targetSerializer.is_valid():
                instance = targetSerializer.create(data)
                return instance
            else:
                return None
        if expectedQueryCount:
            createData = wrapFunctionForQueryCount(expectedQueryCount)(createData)

        instance = None
        testFlag = False
        if serializer.serializer_type == "create":
            instance = createData(serializer, data)
            if instance:
                testFlag = True
        self.assertEqual(expectedResult, testFlag)
        return instance
    