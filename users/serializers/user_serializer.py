from rest_framework import serializers
from ..models import User
from ..dtos import UserDTO


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password"]

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return UserDTO(**data)
