from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions

from ..models import Post
from .serializers import PostSerializer, UserSerializer
from .mixins import LikedMixin


class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    http_method_names = ['post', 'put', 'patch']
