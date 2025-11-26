# Django REST Framework modules
from rest_framework.serializers import ModelSerializer

# Project modules
from django.contrib.auth.models import User


class UserForeignSerializer(ModelSerializer):
    """
    Serializer for User model to be used as a foreign key representation.
    """

    class Meta:
        """Meta class for UserForeignSerializer."""
        model = User
        fields = ['id', 'username', 'email']