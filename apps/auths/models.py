#Python modules
from typing import Any

#Django modules
from django.db.models import (
    EmailField, 
    CharField, 
    BooleanField,
    DateField,
    DecimalField,
)
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

#Project modules
from apps.abstracts.models import AbstractSoftDeletableModel
from apps.auths.validators import validate_not_restricted_email_domain

class CustomUserManager(BaseUserManager):
    """Custom User Manager to make database requests"""

    def __obtain_user_instance(
            self,
            email: str,
            username: str,
            password: str,
            **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Get user instance"""
        if not email:
            raise ValidationError(
                message="The Email field must be set",
            )
        if not username:
            raise ValidationError(
                message="The Username field must be set",
            )
        new_user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
            **kwargs,
        )
        return new_user
    def create_user(
            self,
            email: str,
            username: str,
            password: str,
            **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Create and save a regular user"""
        new_user: 'CustomUser' = self.__obtain_user_instance(
            email=email,
            username=username,
            password=password,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user
    
    def create_superuser(
            self,
            email: str,
            username: str,
            password: str,
            **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Create and save a superuser"""

        new_user = self.__obtain_user_instance(
            email=email,
            username=username,
            password=password,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user
    

class CustomUser(AbstractSoftDeletableModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom user model extending AbstractSoftDeletableModel.
    """

    # Role choices
    ROLE_ADMIN = 'admin'
    ROLE_MANAGER = 'manager'
    ROLE_EMPLOYEE = 'employee'

    ROLE_ADMIN_LABEL = 'Admin'
    ROLE_MANAGER_LABEL = 'Manager'
    ROLE_EMPLOYEE_LABEL = 'Employee'

    ROLE_CHOICES = {
        ROLE_ADMIN: ROLE_ADMIN_LABEL,
        ROLE_MANAGER: ROLE_MANAGER_LABEL,
        ROLE_EMPLOYEE: ROLE_EMPLOYEE_LABEL,   
    }

    MAX_EMAIL_LENGTH = 255
    MAX_NAME_LENGTH = 150
    PASSWORD_MIN_LENGTH = 256
    MAX_CITY_LENGTH = 100

    email = EmailField(
        unique=True,
        max_length=MAX_EMAIL_LENGTH,
        db_index=True,
        validators=[validate_not_restricted_email_domain],
        verbose_name="Email Address",
        help_text="Required. Enter a valid email address.", 
    )
    username = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name="Username",
    )
    first_name = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name="First Name",
        blank=True,
        null=True,
    )
    last_name = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name="Last Name",
        blank=True,
        null=True,
    )
    phone_number = CharField(
        max_length=15,
        verbose_name="Phone Number",
        blank=True,
        null=True,
    )
    city = CharField(
        max_length=MAX_CITY_LENGTH,
        verbose_name="City",
        blank=True,
        null=True,
    )
    country = CharField(
        max_length=MAX_CITY_LENGTH,
        verbose_name="Country",
        blank=True,
        null=True,
    )
    department = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name="Department",
        blank=True,
        null=True,
    )
    role = CharField(
        max_length=20,
        choices=[(key, value) for key, value in ROLE_CHOICES.items()],
        default=ROLE_EMPLOYEE,
        verbose_name="User Role",
    )
    birth_date = DateField(
        blank=True,
        null=True,
        verbose_name="Birth Date",
    )
    salary = DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Salary",
    )
    password = CharField(
        max_length=PASSWORD_MIN_LENGTH,
        validators=[validate_password],
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
    
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()
    
    class Meta:
        """Meta class for CustomUser."""

        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']
    
