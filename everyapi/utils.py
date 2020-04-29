from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from socialdistancing.utils import refractorHour,refractorMinute,checkHour,checkMinute
from socialdistancing.models import *
from usermanagement.models import UserProfile
import datetime
def checkValidToken(token):
    try:
        token = Token.objects.get(key = token)
        return True
    except ObjectDoesNotExist:
        return False


def checkDoctor(user_prof):
    return True if user_prof.user_type == 'Doctor' else False


def checkShopkeeper(user_prof):
    return True if user_prof.user_type == 'Shopkeeper' else False


def save(user_prof,shop_name,location,shop_type,closing_time,opening_time):
    if checkMinute(opening_time) or checkMinute(closing_time):
        return 'Wrong minutes chosen'
    elif checkHour(opening_time) or checkHour(closing_time):
        return 'Wrong hours chosen'
    elif Shop.objects.filter(shop_name=shop_name).exists():
        return 'Wrong shop_name chosen'
    else:
        opening_hour = refractorHour(opening_time)
        opening_minute = refractorMinute(opening_time)
        closing_hour = refractorHour(closing_time)
        closing_minute = refractorMinute(closing_time)
        opening_time = datetime.time(opening_hour,opening_minute)
        closing_time = datetime.time(closing_hour,closing_minute)
        shop = Shop(opening_time = opening_time,closing_time  = closing_time,location = location,shop_type= shop_type,shop_name = shop_name,owner = user_prof)
        shop.save()
        return 'Successfully saved'
def saveRequest(user_prof,shop_id,expected_going_time,expected_leaving_time):
    expected_going_hour = refractorHour(expected_going_time)
    expected_going_minute = refractorMinute(expected_going_time)
    expected_going_time = datetime.time(expected_going_hour, expected_going_minute)
    expected_leaving_hour = refractorHour(expected_leaving_time)
    expected_leaving_minute = refractorMinute(expected_leaving_time)
    expected_leaving_time = datetime.time(expected_leaving_hour, expected_leaving_minute)
    shop = Shop.objects.get(id=int(shop_id))
    if expected_going_time < shop.opening_time:
            # messages.info(request, 'Shop will open after your requested time try to place it after it\'s opening time')
        msg = 'Shop will open after your requested time'
        return msg
    elif expected_going_time > shop.closing_time:
            # messages.info(request, 'Shop Will be closed then')
        msg = 'Shop will open after your requested time'
        return msg
    elif expected_leaving_time > shop.closing_time:
            # messages.info(request, 'Shop Will Close Early')
        msg = 'Shop Will close early'    
        return msg
    else:
        req = Request(shop_name=shop, expected_going_time=expected_going_time, expected_leaving_time = expected_leaving_time, placer = user_prof)
        req.save()
        msg = 'request placed successfully'
        return msg

def updatechanges(opening_time,closing_time,shop):
	if checkHour(opening_time) or checkHour(closing_time):
		return 'Invalid hour chosen'
	elif checkMinute(opening_time) or checkMinute(closing_time):
		return 'Invalid Minute Chosen'
	if opening_time != '' and closing_time != '':
		opening_hour = refractorHour(opening_time)
		opening_minute = refractorMinute(opening_time)
		closing_hour = refractorHour(closing_time)
		closing_minute = refractorMinute(closing_time)
		opening_time = datetime.time(opening_hour,opening_minute)
		closing_time = datetime.time(closing_hour,closing_minute)
		shop.opening_time = opening_time
		shop.closing_time = closing_time
		shop.save()
	elif opening_time!= '' and closing_time == '':
		opening_hour = refractorHour(opening_time)
		opening_minute = refractorMinute(opening_time)
		opening_time = datetime.time(opening_hour,opening_minute)
		shop.opening_time = opening_time
		shop.save()
	elif opening_time== '' and closing_time != '':
		closing_hour = refractorHour(closing_time)
		closing_minute = refractorMinute(closing_time)
		closing_time = datetime.time(closing_hour,closing_minute)
		shop.closing_time = closing_time
		shop.save()