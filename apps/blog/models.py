from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email']


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField()
    likes = GenericRelation(Like)

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()
