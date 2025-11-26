# Python modules
from typing import Any
from urllib import request
from drf_spectacular.utils import OpenApiResponse, extend_schema

# Django modules
from django.contrib.auth.models import User
from django.db.models import QuerySet, Count

# Django REST Framework
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.decorators import action

# Project modules
from apps.courses.models import Course, Lesson
from apps.courses.permissions import IsOwner
from apps.courses.serializers import (
    CourseBaseSerializer, 
    CourseListSerializer, 
    CourseCreateSerializer, 
    CourseUpdateSerializer,
    LessonSerializer,
    LessonCreateSerializer,
    )

class CourseViewSet(ViewSet):
    """
    A viewset for managing courses and lessons.
    """

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Use IsOwner for update and destroy; only IsAuthenticated for others

        if getattr(self, "action", None) in ("update", "destroy"):
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    @extend_schema(
        description="Get a list of all active courses.",
        request=CourseCreateSerializer,
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Successful response with list of courses.",
                response=CourseListSerializer,
            ),
        }
    )

    def list(
        self,
        request: Request,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        List all active courses.
        """
        all_courses: QuerySet[Course] = Course.objects.select_related("owner").annotate(
            lesson_count=Count('lessons')
        ).all()

        serializer = CourseListSerializer(
            all_courses,
            many=True,
        )

        return Response(
            data=serializer.data,
            status=HTTP_200_OK,
        )

    @extend_schema(
        description="Create a new course.",
        request=CourseCreateSerializer,
        responses={
            HTTP_201_CREATED: OpenApiResponse(
                description="Course created successfully.",
                response=CourseCreateSerializer,
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided.",
            ),
        }
    )

    def create(
        self,
        request: Request,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Create a new course.
        """
        serializer: CourseCreateSerializer = CourseCreateSerializer(
            data=request.data,
            context={'request': request},
        )

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )
        
        serializer.save()

        return Response(
            data=serializer.data,
            status=HTTP_201_CREATED,
        )

    @extend_schema(
        description="Retrieve a specific course by its ID.",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Successful response with course details.",
                response=CourseBaseSerializer,
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Course not found.",
            ),
        }
    ) 

    def retrieve(
        self,
        request: Request,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],    ) -> Response:
        """
        Retrieve a specific course by its ID.
        """
        try:
            courses: Course = Course.objects.get(id=kwargs['pk'])
        except Course.DoesNotExist:
            return Response(
                data={"id": [f"Course with id {kwargs['pk']} does not exist."]},
                status=HTTP_404_NOT_FOUND,
            )
        
        serializer: CourseBaseSerializer = CourseBaseSerializer(courses)
        return Response(
            data=serializer.data,
            status=HTTP_200_OK,
        )
    
    @extend_schema(
        description="Update a specific course by its ID.",
        request=CourseUpdateSerializer,
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Course updated successfully.",
                response=CourseUpdateSerializer,
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided.",
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Course not found.",
            ),
        }
    )

    def update(
        self,
        request: Request,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Update a specific course by its ID.
        """
        try:
            course: Course = Course.objects.get(id=kwargs['pk'])
        except Course.DoesNotExist:
            return Response(
                data={"id": [f"Course with id {kwargs['pk']} does not exist."]},
                status=HTTP_404_NOT_FOUND,
            )
        
        self.check_object_permissions(request, course)
        serializer: CourseUpdateSerializer = CourseUpdateSerializer(
            data=request.data,
            instance=course,
            partial=False,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=serializer.data,
            status=HTTP_200_OK,
        )
    
    @extend_schema(
        description="Delete a specific course by its ID.",
        responses={
            HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Course deleted successfully.",
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Course not found.",
            ),
        }
    )

    def destroy(
        self,
        request: Request,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Delete a specific course by its ID.
        """
        try:
            course: Course = Course.objects.get(id=kwargs['pk'])
        except Course.DoesNotExist:
            return Response(
                data={"id": [f"Course with id {kwargs['pk']} does not exist."]},
                status=HTTP_404_NOT_FOUND,
            )
        self.check_object_permissions(request, course)
        
        course.delete()

        return Response(
            status=HTTP_204_NO_CONTENT,
        )
    
    @action(detail=True, methods=['post'])
    @extend_schema(
        description="Activate a specific course by its ID.",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Course activated successfully.",
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Course not found.",
            ),
        }
    )

    def activate(
        self,
        request: Request,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Activate a specific course by its ID.
        """
        try:
            course: Course = Course.objects.get(id=kwargs['pk'])
        except Course.DoesNotExist:
            return Response(
                data={"id": [f"Course with id {kwargs['pk']} does not exist."]},
                status=HTTP_404_NOT_FOUND,
            )
        
        course.is_active = True
        course.save()

        return Response(
            status=HTTP_200_OK,
        )
    
    @action(detail=True, methods=['post'])
    @extend_schema(
        description="Deactivate a specific course by its ID.",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Course deactivated successfully.",
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Course not found.",
            ),
        }
    )

    def deactivate(
        self,
        request: Request,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Deactivate a specific course by its ID.
        """
        try:
            course: Course = Course.objects.get(id=kwargs['pk'])
        except Course.DoesNotExist:
            return Response(
                data={"id": [f"Course with id {kwargs['pk']} does not exist."]},
                status=HTTP_404_NOT_FOUND,
            )
        
        course.is_active = False
        course.save()

        return Response(
            status=HTTP_200_OK,
        )
    
    @extend_schema(
        description="List all lessons for a specific course.",
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Lessons retrieved successfully.",
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Course not found.",
            ),
        }
    )

    @action(
        methods=['get'],
        detail=True,
        url_path='lessons',
        url_name='list-lessons',
        permission_classes=[IsAuthenticated],
    )
    def list_lessons(
        self,
        request: Request,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        List all lessons for a specific course.
        """
        try:
            course: Course = Course.objects.get(id=kwargs['pk'])
        except Course.DoesNotExist:
            return Response(
                data={"id": [f"Course with id {kwargs['pk']} does not exist."]},
                status=HTTP_404_NOT_FOUND,
            )
        
        self.check_object_permissions(request, course)

        return Response(
            data=LessonSerializer(
                course.lessons.all(),
                many=True,
            ).data,
            status=HTTP_200_OK,
        )
    

class LessonViewSet(ViewSet):
    """
    A viewset for managing lessons.
    """

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Use IsOwner for actions that modify lessons
        if getattr(self, "action", None) in ("move_lesson", "destroy_lesson", "publish_lesson", "unpublish_lesson"):
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]
    
    @extend_schema(
        description="Create a new lesson for a specific course.",
        request=LessonCreateSerializer,
        responses={
            HTTP_201_CREATED: OpenApiResponse(
                description="Lesson created successfully.",
                response=LessonCreateSerializer,
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided.",
            ),
        }
    )

    def create_lesson(
        self,
        request: Request,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Create a new lesson for a specific course.
        """

        try: 
            course: Course = Course.objects.get(id=kwargs['course_pk'])
        except Course.DoesNotExist:
            return Response(
                data={"course_id": [f"Course with id {kwargs['course_pk']} does not exist."]},
                status=HTTP_404_NOT_FOUND,
            )
        self.check_object_permissions(request, course)
        serializer: LessonCreateSerializer = LessonCreateSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )
        serializer.save(course=course)

        return Response(
            data=serializer.data,
            status=HTTP_201_CREATED,
        )
    
    @extend_schema(
        description="Delete a specific lesson by its ID.",
        responses={
            HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Lesson deleted successfully.",
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Lesson not found.",
            ),
        }
    )

    @action(
        methods=['put'],
        detail=True,
        url_path='move',
        url_name='move-lesson',
        permission_classes=[IsAuthenticated, IsOwner],
    )
    def move_lesson(
        self,
        request: Request,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Move a specific lesson to a different course.
        """
        try:
            lesson: Lesson = Lesson.objects.get(id=kwargs['pk'])
        except Lesson.DoesNotExist:
            return Response(
                data={"id": [f"Lesson with id {kwargs['pk']} does not exist."]},
                status=HTTP_404_NOT_FOUND,
            )
        self.check_object_permissions(request, lesson.course)

        before_id = request.data.get('before_lesson_id', None)

        siblings = list(lesson.course.lessons.filter(deleted_at__isnull=True).exclude(id=lesson.id).order_by('order'))

        insert_index = None
        if before_id is not None:
            try:
                before_id = int(before_id)
            except (TypeError, ValueError):
                return Response({'before_lesson_id': ['Invalid id']}, status=HTTP_400_BAD_REQUEST)

            before_lesson = next((l for l in siblings if l.id == before_id), None)
            if before_lesson is None:
                return Response({'before_lesson_id': [f'Lesson with id {before_id} not found in the same course']}, status=HTTP_400_BAD_REQUEST)

            for idx, s in enumerate(siblings):
                if s.id == before_id:
                    insert_index = idx
                    break


        new_sequence = []
        if insert_index is None:
            new_sequence = siblings + [lesson]
        else:
            new_sequence = siblings[:insert_index] + [lesson] + siblings[insert_index:]

        from decimal import Decimal
        new_order = None
        for pos, l in enumerate(new_sequence, start=1):
            order_value = Decimal(pos).quantize(Decimal('1.00'))
            if l.id == lesson.id:
                new_order = order_value
                if pos > 1:
                    prev = new_sequence[pos-2]
                    lesson.indentation = prev.indentation
                else:
                    lesson.indentation = 0
                lesson.order = order_value
                lesson.save(update_fields=['order', 'indentation'])
            else:
                if l.order != order_value:
                    l.order = order_value
                    l.save(update_fields=['order'])

        return Response({'order': str(new_order)}, status=HTTP_200_OK)
        

    @action(
        methods=['delete'],
        detail=True,
        url_path='delete',
        url_name='destroy-lesson',
        permission_classes=[IsAuthenticated, IsOwner],
    )
    @extend_schema(
        description="Delete a specific lesson by its ID.",
        responses={
            HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Lesson deleted successfully.",
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Lesson not found.",
            ),
        }
    )
    def destroy_lesson(
        self,
        request: Request,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Delete a specific lesson by its ID.
        """
        try:
            lesson: Lesson = Lesson.objects.get(id=kwargs['pk'])
        except Lesson.DoesNotExist:
            return Response(
                data={"id": [f"Lesson with id {kwargs['pk']} does not exist."]},
                status=HTTP_404_NOT_FOUND,
            )
        self.check_object_permissions(request, lesson.course)
        
        lesson.delete()

        return Response(
            status=HTTP_204_NO_CONTENT,
        )
    
    @action(
        methods=['post'],
        detail=True,
        url_path='publish',
        url_name='publish-lesson',
        permission_classes=[IsAuthenticated, IsOwner],
    )
    @extend_schema(
            description="Publish a specific lesson by its ID.",
            responses={
                HTTP_200_OK: OpenApiResponse(
                    description="Lesson published successfully.",
                ),
            }
    )
    def publish_lesson(
        self, 
        request: Request,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Publish a specific lesson by its ID.
        """
        try:
            lesson: Lesson = Lesson.objects.get(id=kwargs['pk'])
        except Lesson.DoesNotExist:
            return Response(
                data={"id": [f"Lesson with id {kwargs['pk']} does not exist."]},
                status=HTTP_404_NOT_FOUND,
            )
        self.check_object_permissions(request, lesson.course)
        
        lesson.is_published = True
        lesson.save()

        return Response(
            status=HTTP_200_OK,
        )

    @action(
        methods=['post'],
        detail=True,
        url_path='unpublish',
        url_name='unpublish-lesson',
        permission_classes=[IsAuthenticated, IsOwner],
    )
    @extend_schema(
            description="Unpublish a specific lesson by its ID.",
            responses={
                HTTP_200_OK: OpenApiResponse(
                    description="Lesson unpublished successfully.",
                ),
            }
    )
    def unpublish_lesson(
        self, 
        request: Request,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
    ) -> Response:
        """
        Unpublish a specific lesson by its ID.
        """
        try:
            lesson: Lesson = Lesson.objects.get(id=kwargs['pk'])
        except Lesson.DoesNotExist:
            return Response(
                data={"id": [f"Lesson with id {kwargs['pk']} does not exist."]},
                status=HTTP_404_NOT_FOUND,
            )
        self.check_object_permissions(request, lesson.course)
        
        lesson.is_published = False
        lesson.save()

        return Response(
            status=HTTP_200_OK,
        ) 