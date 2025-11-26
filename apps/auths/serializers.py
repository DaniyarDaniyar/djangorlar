from typing import Any, Optional

from rest_framework.serializers import (
    Serializer,
    CharField,
    ListField,
)
from rest_framework.exceptions import ValidationError

from django.contrib.auth.models import User


class UserLoginResponseSerializer(Serializer):
    username = CharField(required=True)
    password = CharField(required=True, write_only=True)
    access = CharField()
    refresh = CharField()


class UserLoginErrorsSerializer(Serializer):
    username = ListField(child=CharField(), required=False)
    password = ListField(child=CharField(), required=False)


class HTTP405MethodNotAllowedSerializer(Serializer):
    detail = CharField()


class UserLoginSerializer(Serializer):
    USERNAME_MAX_LENGTH = 150
    PASSWORD_MAX_LENGTH = 128

    username = CharField(required=True, max_length=USERNAME_MAX_LENGTH)
    password = CharField(required=True, max_length=PASSWORD_MAX_LENGTH, write_only=True)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        username: str = attrs.get("username")
        password: str = attrs.get("password")

        user: Optional[User] = User.objects.filter(username=username).first()
        if user is None:
            raise ValidationError({"username": ["User with this username does not exist."]})
        if not user.check_password(password):
            raise ValidationError({"password": ["Incorrect password."]})
        attrs["user"] = user
        return super().validate(attrs)
