import os
import clearbit

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from typing import Union
from .models import Like
from pyhunter import PyHunter

User = get_user_model()


def add_like(obj, user) -> None:
    """
    Mark as liked.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user)
    return like


def remove_like(obj, user) -> None:
    """
    Unmark as liked.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    ).delete()


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


def is_verified(email: str) -> bool:
    """
    Verifying the deliverability of an email address through hunter.io
    """
    api_key: str = os.getenv('HUNTER_API_KEY')
    hunter: PyHunter = PyHunter(api_key)
    try:
        result: dict = hunter.email_verifier(email)
    except Exception:
        # DO CARE ABOUT EXCEPTION HANDLING
        return False

    status: str = result.get('status')

    # HERE IS SHOULD BE ANY VALIDATION

    if status in ('valid', 'accept_all', 'webmail'):
        return True
    return False


def get_additional_data(email: str) -> Union[dict, None]:
    """
    Getting user info from clearbit
    """
    clearbit.key = os.getenv('CLEARBIT_API_KEY')
    try:
        response: dict = clearbit.Enrichment.find(email=email, stream=True)
    except Exception:
        # DO CARE ABOUT EXCEPTION HANDLING
        return None

    return response['person'] if 'person' in response else None



