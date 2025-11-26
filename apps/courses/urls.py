# Django modules
from django.urls import path, include

# Django REST Framework modules
from rest_framework.routers import DefaultRouter

# Project modules
from apps.courses.views import CourseViewSet, LessonViewSet

router: DefaultRouter = DefaultRouter(
    trailing_slash=False,
)

router.register(
    prefix='courses',
    viewset=CourseViewSet,
    basename='courses',
)
router.register(
    prefix='lessons',
    viewset=LessonViewSet,
    basename='lessons',
)

urlpatterns = [
    path('', include(router.urls)),

]