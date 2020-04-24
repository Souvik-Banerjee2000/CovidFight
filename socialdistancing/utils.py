from .models import Shop,Request
import datetime
from django.contrib import messages
from django.shortcuts import redirect
from usermanagement.models import UserProfile
from django.http import HttpResponseRedirect


def refractorMinute(passed_time):
	passed_time = passed_time.split(':')
	passed_minute = int(passed_time[1])
	return passed_minute


def refractorHour(passed_time):
	passed_time = passed_time.split(':')
	passed_hour = int(passed_time[0])
	return passed_hour


def checkHour(passed_time): #if the hour is invalid returns true
	if refractorHour(passed_time) > 24:
		return True
	return False


def checkMinute(passed_time): #IF the nimute is invalid returns true
	if refractorMinute(passed_time) > 60:
		return True 
	return False





def save(request,opening_time,closing_time,location,shop_name,shop_type):
	if checkMinute(opening_time) or checkMinute(closing_time) :
		messages.error(request,'Invalid minute chosen')
		return redirect('/createshop')
	elif checkHour(opening_time) or checkHour(closing_time) :
		messages.error(request,'Invalid hour chosen')
		return redirect('/createshop')
	elif Shop.objects.filter(shop_name = shop_name).exists():
		messages.error(request,'This Shop Name Already exists choose a different one')
		return redirect('/createshop')
	else:
		opening_hour = refractorHour(opening_time)
		opening_minute = refractorMinute(opening_minute)
		closing_hour = refractorHour(closing_time)
		closing_minute = refractorMinute(closing_time)
		user = request.user
		user_prof = UserProfile.objects.get(user = user)
		opening_time = datetime.time(opening_hour,opening_minute)
		closing_time = datetime.time(closing_hour,closing_minute)
		shop = Shop(opening_time = opening_time,closing_time  = closing_time,location = location,shop_type= shop_type,shop_name = shop_name,owner = user_prof)
		shop.save()

def updatechanges(request,opening_time,closing_time,id):
	if checkHour(opening_time) or checkHour(closing_time):
		messages.error(request,'Invalid hour chosen')
		return redirect('/createshop')
	elif checkMinute(opening_time) or checkMinute(closing_time):
		messages.error(request,'Invalid Minute Chosen')
		return redirect('/createshop')
	shop = Shop.objects.get(id = id)
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

def saveRequest(request,id,expected_going_time,expected_leaving_time):
	expected_going_hour = refractorHour(expected_going_time)
	expected_going_minute = refractorMinute(expected_going_time)
	expected_going_time = datetime.time(expected_going_hour,expected_going_minute)
	expected_leaving_hour = refractorHour(expected_leaving_time)
	expected_leaving_minute = refractorMinute(expected_leaving_time)
	expected_leaving_time = datetime.time(expected_leaving_hour,expected_leaving_minute)
	shop = Shop.objects.get(id = int(id))
	if expected_going_time < shop.opening_time:
		messages.info(request,'Shop will open after your requested time try to place it after it\'s opening time')
		return False
	elif expected_going_time > shop.closing_time:
		messages.info(request,'Shop Will be closed then')
		return False
	elif expected_leaving_time > shop.closing_time:
		messages.info(request,'Shop Will Close Early')
		return False
	else:
		user_prof = UserProfile.objects.get(user = request.user)
		req = Request(shop_name = shop,expected_going_time = expected_going_time,expected_leaving_time = expected_leaving_time,placer = user_prof)
		req.save()
		return True


			


