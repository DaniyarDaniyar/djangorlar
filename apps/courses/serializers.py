# Django REST Framework modules
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    Field,
)

# Project modules
from apps.courses.models import Course, Lesson
from apps.abstract.serializers import UserForeignSerializer

class CourseBaseSerializer(ModelSerializer):
    """
    Base serializer for Course model.
    """

    class Meta:
        model = Course
        fields = "__all__"


class CourseListSerializer(CourseBaseSerializer):
    """
    Serializer for listing courses with lesson count.
    """

    lesson_count = SerializerMethodField(
        method_name='get_lesson_count',
    )
    owner = UserForeignSerializer()

    class Meta:
        """Meta class for CourseListSerializer."""
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'owner',
            'is_active',
            'lesson_count',
        ]
    
    def get_lesson_count(self, obj: Course) -> int:
        """
        Get the count of lessons for the course.
        """
        return getattr(obj, 'lesson_count', 0)
    

class CourseCreateSerializer(CourseBaseSerializer):
    """
    Serializer for creating a new course.
    """

    class Meta:
        """Meta class for CourseCreateSerializer."""
        model = Course
        fields = [
            'title',
            'description',
            'is_active',
        ]

    def create(self, validated_data):
        """Set owner from request context."""
        request = self.context.get('request')
        if request:
            validated_data['owner'] = request.user
        return super().create(validated_data)


class CourseUpdateSerializer(CourseBaseSerializer):
    """Serializer used for updating a course (full update)."""

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'is_active',
        ]


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'content',
            'order',
            'indentation',
            'is_published',
            'created_at',
            'updated_at',
        ]


class LessonCreateSerializer(LessonSerializer):
    class Meta:
        model = Lesson
        fields = [
            'title',
            'content',
            'indentation',
            'is_published',
        ]

    