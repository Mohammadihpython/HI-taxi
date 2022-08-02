from celery import shared_task

"""

I Use kavenegar service for send sms to user
Use your Api Key
"""
from kavenegar import *
from django.conf import settings

try:
    import json
except ImportError:
    import simplejson as json


@shared_task
def send_sms(
        phone_number,
        code,
        code_type,
):
    try:
        api = KavenegarAPI(settings.APIKEY)
        print(api)
        params = {
            'sender':'Hamed',
            'receptor': f'{phone_number}',
            'message': f'سلام کاربر گرامی کد {code_type}شما:{code}'
        }
        response = api.sms_send(params)
        print("yes")
        return response
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
