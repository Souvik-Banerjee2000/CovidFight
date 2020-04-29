from socialdistancing.models import  *
from .serializer import ShopSerializer,RequestSerializer,NotificationSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

from rest_framework.parsers import JSONParser
from usermanagement.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from .utils import checkValidToken,checkShopkeeper,save,saveRequest,updatechanges


@api_view(['GET'],)
def allShops(request):
    shops = Shop.objects.all()
    serializer = ShopSerializer(shops,many = True)
    return JsonResponse(serializer.data,safe = False)

@api_view(['GET'],)
def searchbyLocation(request,location):
    try:
        shops = Shop.objects.filter(location__icontains = location)
    except ObjectDoesNotExist:
        return JsonResponse('No shops in this location',safe  = False)

    serializer = ShopSerializer(shops, many = True)
    return JsonResponse(serializer.data,safe=False)

@api_view(['GET'],)
def searchbyName(request,name):
    try:
        shops = Shop.objects.filter(shop_name__icontains = name)
    except ObjectDoesNotExist:
        return JsonResponse('No shops with this name',safe  = False)    
    seirializer = ShopSerializer(shops,many = True)
    return JsonResponse(seirializer.data,safe = False)


@api_view(['GET'],)
def searchbyType(request,type):
    try:
        shops = Shop.objects.filter(shop_type__icontains=type)
    except ObjectDoesNotExist:
        return JsonResponse('No shops in this location',safe  = False)
    seirializer = ShopSerializer(shops, many=True)
    return JsonResponse(seirializer.data, safe=False)


@api_view(['POST'],)
def createShop(request,token):
    if checkValidToken(token):
        user = Token.objects.get(key=str(token)).user
        user_prof = UserProfile.objects.get(user = user)
        if checkShopkeeper(user_prof):
            data = JSONParser().parse(request)
            msg = save(user_prof,data['shop_name'],data['location'],data['shop_type'],data['closing_time'],data['opening_time'])
            return JsonResponse(msg,safe=False)
        return JsonResponse('Only Shopkeepers can create shops',safe = False)   
    return JsonResponse('Invalid Token Provided',safe = False)             


@api_view(['POST'],)
def placeRequest(request,token,shop_id):
    if checkValidToken(token):
        user = Token.objects.get(key = str(token)).user
        user_prof = UserProfile.objects.get(user = user)
        shop = Shop.objects.get(id = shop_id)
        if shop.owner != user_prof:
            data = JSONParser().parse(request)
            msg = saveRequest(user_prof,shop_id,data['expected_going_time'],data['expected_leaving_time'])
            return JsonResponse(msg,safe = False)
        else:
            return JsonResponse('Why you are trying to place requests to your own shop',safe = False)    
    return JsonResponse('Invalid token provided',safe=False)    

@api_view(['GET'],)
def seeallShops(request,token):
    user_prof = UserProfile.objects.get(user = Token.objects.get(key=str(token)).user)
    if checkShopkeeper(user_prof):
        shops = Shop.objects.filter(owner = user_prof)
        serializer = ShopSerializer(shops,many = True)
        return JsonResponse(serializer.data,safe = False)
    return JsonResponse('you are not a shopkeeper',safe = False)    



@api_view(['GET'],)    #To see all the requests have been placed to a particular shop
def seeallRequests(request,token,shop_id):
    user = Token.objects.get(key=str(token)).user
    user_prof = UserProfile.objects.get(user = user)
    if checkShopkeeper(user_prof):
        shop = Shop.objects.get(id = shop_id)
        if shop.owner == user_prof:
            re = Request.objects.filter(shop_name = shop)
            serializer = RequestSerializer(re,many = True) #Returns Empty array if any requests have not been placed yet in this shop
            return JsonResponse(serializer.data,safe = False)
        else:
            return JsonResponse('You are not the owner of this particular shop',safe = False)    
    return JsonResponse('You are not a shopkeeper',safe = False)    

@api_view(['POST'])
def accept_or_decline(request,token,shop_id,request_id):
    user = Token.objects.get(key=str(token)).user
    user_prof = UserProfile.objects.get(user=user)
    if checkShopkeeper(user_prof):
        shop = Shop.objects.get(id = shop_id)
        re = Request.objects.get(id = request_id)
        if re.shop_name == shop:
            placer = re.placer
            data = JSONParser().parse(request)
            status = True if data['status'] == 'accepted' else False
            no = Notifiaction.objects.create(user_prof = placer,status = status,message = data['message'])    
            re.delete()
            return JsonResponse(data['status'],safe = False)
        return JsonResponse('You are trying to access a shop which is not yours',safe = False)
    return JsonResponse('You are not a shopkeeper',safe = False)        
    
@api_view(['GET'],)
def view_users_request(request,token):  #All the request that are available for a particular user
    user = Token.objects.get(key=str(token)).user
    user_prof = UserProfile.objects.get(user=user) 
    re = Request.objects.filter(placer = user_prof)
    serializer = RequestSerializer(re,many = True)
    return JsonResponse(serializer.data,safe = False)

@api_view(['GET'],)
def view_user_notifications(request,token): #All the notifications available for a particular user
    user = Token.objects.get(key=str(token)).user
    user_prof = UserProfile.objects.get(user=user)
    no = Notifiaction.objects.filter(user_prof = user_prof)
    serializer = NotificationSerializer(no,many = True)
    return JsonResponse(serializer.data,safe = False)

@api_view(['DELETE'],)
def delete_users_requests(request,token,request_id):
    user_prof = UserProfile.objects.get(user=Token.objects.get(key=str(token)).user)
    re = Request.objects.get(id = request_id)
    if re.placer == user_prof:
        re.delete()
        return JsonResponse('request Deleted',safe = False)
    return JsonResponse('You should try to delete your own request',safe = False)

@api_view(['DELETE'],)
def delete_users_notifications(request,token,notification_id):
    user_prof = UserProfile.objects.get(user=Token.objects.get(key=str(token)).user)
    no = Notifiaction.objects.get(id = notification_id)
    if no.user_prof == user_prof:
        no.delete()
        return JsonResponse('Notification Deleted', safe=False)
    return JsonResponse('You should try to delete your own request', safe=False)

@api_view(['PUT'],)
def updateshop(request,token,shop_id):
    user_prof = UserProfile.objects.get(user=Token.objects.get(key=str(token)).user)
    shop = Shop.objects.get(id = shop_id)
    if shop.owner == user_prof:
        data = JSONParser().parse(request)
        msg = updatechanges(data['opening_time'],data['closing_time'],shop)
        if msg is None:
            return JsonResponse('Updated successfully',safe = False)
        return JsonResponse(msg,safe = False)
    return JsonResponse('You do not have permissions to do this',safe = False)    



