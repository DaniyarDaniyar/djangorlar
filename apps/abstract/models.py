#Python modules
from typing import Any

#Django modules
from django.db.models import Model, DateTimeField
from django.utils import timezone 


class AbstractBaseModel(Model):
    """
    An abstract base model that provides common fields and methods for other models.
    """

    created_at = DateTimeField(
        auto_now_add=True,
    )
    updated_at = DateTimeField(
        auto_now=True,
    )
    deleted_at = DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        """Make this model abstract so it won't create a database table."""
        
        abstract = True

    def delete(self, *args: tuple[Any, ...], **kwargs: dict[Any, Any]) -> None:
        """
        Soft delete the model instance by setting the deleted_at field to the current time.
        """

        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

