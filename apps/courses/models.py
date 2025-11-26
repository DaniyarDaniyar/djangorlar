# Python modules

#Django modules
from django.db.models import (
    CharField,
    TextField,
    ForeignKey,
    CASCADE,
    IntegerField,
    BooleanField,
    DecimalField,
)
from django.contrib.auth.models import User

#Project modules
from apps.abstract.models import AbstractBaseModel

class Course(AbstractBaseModel):
    """
    Model representing a course.
    """
    TITLE_MAX_LENGTH = 255

    title = CharField(
        max_length=TITLE_MAX_LENGTH,
    )
    description = TextField(
        blank=True,
    )
    owner = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='owned_courses',
    )
    is_active = BooleanField(
        default=True,
    )

    def __str__(self) -> str:
        """
        Return a string representation of the course.
        """
        return self.title
    
class Lesson(AbstractBaseModel):
    """
    Model representing a lesson within a course.
    """

    TITLE_MAX_LENGTH = 255
    INDENTATION_MAX_LENGTH = 5

    title = CharField(
        max_length=TITLE_MAX_LENGTH,
    )
    content = TextField(
        blank=True,
    )
    course = ForeignKey(
        Course,
        on_delete=CASCADE,
        related_name='lessons',
    )
    order = DecimalField(
        default=1.0,
        max_digits=5,
        decimal_places=2,
    )
    indentation = IntegerField(
        default=0,
    )
    is_published = BooleanField(
        default=False,
    )

    def __str__(self) -> str:
        """
        Return a string representation of the lesson.
        """
        return f"{self.order}. {self.title}"
    

    
