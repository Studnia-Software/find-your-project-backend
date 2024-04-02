from rest_framework import serializers
from users.models import User
from users.dtos import UserDTO


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password"]

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, email):
        user = User.objects.filter(email=email)
        if user.exists():
            raise serializers.ValidationError("User with this email already exists")

        return email

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return UserDTO(**data)
