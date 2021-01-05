from django.urls import include, path
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from .viewsets import PostViewSet, UserViewSet

router = routers.DefaultRouter()

router.register('post', PostViewSet)
router.register('user', UserViewSet)

schema_view = get_schema_view()

urlpatterns = [
    path('', include(router.urls)),
    path('schema/', schema_view),
]
