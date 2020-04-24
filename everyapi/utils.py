
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
def checkValidToken(token):
    try:
        token = Token.objects.get(key = token)
        return True
    except ObjectDoesNotExist:
        return False


def checkDoctor(user_prof):
    return True if user_prof.user_type == 'Doctor' else False
