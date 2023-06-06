from rest_framework import serializers
from core.serializers import CreateSerializer

from members.models import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            "id",
            "phone",
            # password is write only field
        ]
        read_only_fields = fields

class MemberCreateSerializer(CreateSerializer):
    # CreateSerializer의 to_representation 메서드를 설정하기 위해 필요합니다.
    representation_serializer_class = MemberSerializer
    password2 = serializers.CharField(required=True)

    class Meta:
        model = Member
        fields = (
            "phone",
            "password",
            "password2",
        )
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "This is different with password."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        return Member.objects.createMember(**validated_data)
