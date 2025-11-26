# Django modules
from django.urls import path, include

# Django REST Framework modules
from rest_framework.routers import DefaultRouter

# Project modules
from apps.auths.views import AuthViewSet

router: DefaultRouter = DefaultRouter(
    trailing_slash=False,
)

router.register(
    prefix='auth',
    viewset=AuthViewSet,
    basename='auth',
)

urlpatterns = [
    path('v1/', include(router.urls)),
]