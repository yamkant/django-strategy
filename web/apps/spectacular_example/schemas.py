from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema_view

USER_QUERY_PARAM_USERNAME_EXAMPLES = [
    OpenApiExample(
        "username 필드 필터링을 위한 query parameter 예시입니다.",
        summary="example username 1",
        description="첫 번째 유저명입니다.",
        value="김예함",
    ),
    OpenApiExample(
        "username 필드 필터링을 위한 query parameter 예시입니다.",
        summary="example username 2",
        description="두 번째 유저명입니다.",
        value="김예함",
    ),
]

USER_QUERY_PARAM_DATE_JOINED_EXAMPLES = [
    OpenApiExample(
        "date_joined 필드 필터링을 위한 query parameter 예시입니다.",
        summary="example date_joined 1",
        description="첫 번째 가입일입니다.",
        value="1995-07-08",
    ),
    OpenApiExample(
        "date_joined 필드 필터링을 위한 query parameter 예시입니다.",
        summary="example date_joined 2",
        description="두 번째 가입일입니다.",
        value="1995-07-09",
    ),
]

USER_CREATE_EXAMPLES = [
    OpenApiExample(
        request_only=True,
        summary="성공적으로 생성하는 경우",
        name="success_example",
        value={
            "username": "yamkim",
            "password": "test123!",
            "first_name": "YEHAM",
            "last_name": "KIM",
            "email": "user@example.com",
        },
    ),
    OpenApiExample(
        request_only=True, # 요청시에만 사용가능한 예제로 명시한다.
        summary="비밀번호 너무 쉬움",
        name="invalid_example_too_easy_password",
        value={
            "username": "yamkim",
            "password": "1234",
            "first_name": "YEHAM",
            "last_name": "KIM",
            "email": "user@example.com",
        },
    ),
    OpenApiExample(
        request_only=True,
        summary="이름 필수 입력",
        name="invalid_example_empty_name",
        value={
            "username": "root434",
            "password": "test123!",
            "first_name": "",
            "last_name": "KIM",
            "email": "user@example.com",
        },
    ),
]
