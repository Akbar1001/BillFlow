from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone_number",
            "email_verified",
            "date_joined",
        )


class RegisterSerializer(serializers.ModelSerializer):

    username = serializers.CharField(min_length=4)

    password = serializers.CharField(
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "phone_number",
        )

    def create(self, validated_data):

        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            phone_number=validated_data.get(
                "phone_number",
                ""
            )
        )

        user.set_password(
            validated_data["password"]
        )

        user.save()

        return user