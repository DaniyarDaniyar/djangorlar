#Python modules

#Django modules
from django.db.models import EmailField, CharField, BooleanField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

#Project modules
from apps.abstracts.models import AbstractSoftDeletableModel
from apps.auths.validators import validate_not_restricted_email_domain

class CustomUser(AbstractSoftDeletableModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom user model extending AbstractSoftDeletableModel.
    """
    MAX_EMAIL_LENGTH = 255
    MAX_NAME_LENGTH = 150
    PASSWORD_MIN_LENGTH = 256

    email = EmailField(
        unique=True,
        max_length=MAX_EMAIL_LENGTH,
        db_index=True,
        validators=[validate_not_restricted_email_domain],
        verbose_name="Email Address",
        help_text="Required. Enter a valid email address.", 
    )
    full_name = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name="Full Name",
    )
    password = CharField(
        max_length=PASSWORD_MIN_LENGTH,
        verbose_name="Password",
        help_text="Required. Enter a secure password.",
    )
    is_active = BooleanField(
        default=True,
        verbose_name="Active Status",
        help_text="Designates whether this user should be treated as active.",
    )
    is_staff = BooleanField(
        default=False,
        verbose_name="Staff Status",
        help_text="Designates whether the user can log into this admin site.",
    )
    
    REQUIRED_FIELDS = ['full_name']
    USERNAME_FIELD = 'email'
    
    class Meta:
        """Meta class for CustomUser."""

        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']
    
