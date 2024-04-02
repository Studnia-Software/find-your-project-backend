from rest_framework import serializers
from users.models import User


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("No user with such email exists")

        return email

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return data
