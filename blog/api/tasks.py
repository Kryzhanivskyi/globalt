import os
import clearbit

from django.contrib.auth import get_user_model

from celery import shared_task
from pyhunter import PyHunter


@shared_task
def add_email_status(**kwargs) -> dict:
    """
    Verifying the deliverability of an email address through hunter.io
    """
    api_key: str = os.getenv('HUNTER_API_KEY')
    UserModel = get_user_model()
    hunter: PyHunter = PyHunter(api_key)
    user: UserModel = UserModel.objects.get(username=kwargs.get('username'))
    try:
        result: dict = hunter.email_verifier(kwargs.get('email'))
        if result:
            try:
                user.email_status = result.get('status')
                user.save()
            except KeyError:
                # DO CARE ABOUT EXCEPTION HANDLING
                return {'success': False}
    except Exception:
        # DO CARE ABOUT EXCEPTION HANDLING
        return {'success': False}
    return {'success': True}


@shared_task
def add_additional_data(**kwargs) -> dict:
    """
    Adding additional user info from clearbit
    """
    clearbit.key = os.getenv('CLEARBIT_API_KEY')
    UserModel = get_user_model()
    user: UserModel = UserModel.objects.get(id=kwargs.get('user_id'))
    try:
        response: dict = clearbit.Enrichment.find(email=user.email, stream=True)
        if response and 'person' in response:
            try:
                user.first_name = response['person']['name']['givenName']
                user.last_name = response['person']['name']['familyName']
                user.save()
            except KeyError:
                # DO CARE ABOUT EXCEPTION HANDLING
                return {'success': False}
    except Exception:
        # DO CARE ABOUT EXCEPTION HANDLING
        return {'success': False}
    return {'success': True}



