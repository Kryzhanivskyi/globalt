from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from .models import Like


User = get_user_model()


def add_like(obj, user):
    """
    Mark as liked.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.get_or_create(content_type=obj_type, object_id=obj.id, user=user)
    return {'success': 'True'}


def remove_like(obj, user) -> None:
    """
    Unmark as liked.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user).delete()


def is_liked(obj, user) -> bool:
    """
    Check if already liked.
    """
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()



