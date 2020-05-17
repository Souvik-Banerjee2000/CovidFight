from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.http import JsonResponse
from usermanagement.models import UserProfile
from socialdistancing.models import *
from awareness.models import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view


@api_view(['GET'],)
def giveUserName(request,user_id):
    try:
        user = User.objects.get(id = user_id)
    except ObjectDoesNotExist:
        return JsonResponse({'username':"Wrong id given"},safe = False)
    return JsonResponse({'username':user.username},safe = False)


@api_view(['GET'],)
def giveuserType(request,user_id):
    try:
        user_prof = UserProfile.objects.get(user = User.objects.get(id = user_id))
    except ObjectDoesNotExist:
        return JsonResponse({'username': "No profile with this id"}, safe=False)
    return JsonResponse({'type is':user_prof.user_type},safe = False)


@api_view(['GET'],)
def giveshopname(request,shop_id):
    try:
        shop = Shop.objects.get(id = shop_id)
    except ObjectDoesNotExist:
        return JsonResponse({'shop': "No shop with this id"}, safe=False)
    return JsonResponse({'id':shop.shop_name},safe = False)

@api_view(['GET'],)
def giverequestPlacerName(request,request_id):
    try:
        re = Request.objects.get(id = request_id)
    except ObjectDoesNotExist:
        return JsonResponse({'request': "No request with this id"}, safe=False)    
    return JsonResponse({'name':re.placer.user.username},safe = False) 

@api_view(['GET'],)
def givepostName(request, post_id):
    try:
        post = Post.objects.get(id = post_id)
    except ObjectDoesNotExist:
        return JsonResponse({'post': "No posts"}, safe=False)   
    
    return JsonResponse({'name':post.title},safe = False)        






