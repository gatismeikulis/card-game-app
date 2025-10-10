from typing import Any, override
from rest_framework.serializers import ModelSerializer
from .models import User


class UserListSerializer(ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["id", "screen_name"]


class UserDetailSerializer(ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["id", "screen_name", "description", "date_joined"]
        read_only_fields = ["date_joined"]


class UserFullSerializer(ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "screen_name", "description"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
            "screen_name": {"required": True, "min_length": 5},
        }

    @override
    def create(self, validated_data: dict[str, Any]):
        # .create_user is special method which hashes the password internally and does other magic behind the scenes
        return User.objects.create_user(**validated_data)

    @override
    def update(self, instance: User, validated_data: dict[str, Any]):
        # Handle password hashing if password is updated, because simple update would not hash password
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
