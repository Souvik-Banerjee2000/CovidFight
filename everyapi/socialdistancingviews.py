from socialdistancing.models import  *
from .serializer import ShopSerializer,RequestSerializer,NotificationSerializer
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

from rest_framework.parsers import JSONParser
from usermanagement.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from .utils import checkValidToken,checkShopkeeper,save,saveRequest,updatechanges

from rest_framework.permissions import IsAuthenticated


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
        return JsonResponse({'msg':'No shops in this location'},safe  = False)

    serializer = ShopSerializer(shops, many = True)
    return JsonResponse(serializer.data,safe=False)

@api_view(['GET'],)
def searchbyName(request,name):
    try:
        shops = Shop.objects.filter(shop_name__icontains = name)
    except ObjectDoesNotExist:
        return JsonResponse({'msg':'No shops with this name'},safe  = False)    
    seirializer = ShopSerializer(shops,many = True)
    return JsonResponse(seirializer.data,safe = False)


@api_view(['GET'],)
def searchbyType(request,type):
    try:
        shops = Shop.objects.filter(shop_type__icontains=type)
    except ObjectDoesNotExist:
        return JsonResponse({'msg':'No shops in this location'},safe  = False)
    seirializer = ShopSerializer(shops, many=True)
    return JsonResponse(seirializer.data, safe=False)


@api_view(['POST'],)
@permission_classes([IsAuthenticated])
def createShop(request):
    user_prof = UserProfile.objects.get(user = request.user)
    if checkShopkeeper(user_prof):
        data = JSONParser().parse(request)
        msg = save(user_prof,data['shop_name'],data['location'],data['shop_type'],data['closing_time'],data['opening_time'])
        return JsonResponse({'msg':msg},safe=False)
    return JsonResponse({'msg':'Only Shopkeepers can create shops'},safe = False)   
             


@api_view(['POST'],)
@permission_classes([IsAuthenticated])
def placeRequest(request,shop_id):
    user_prof = UserProfile.objects.get(user = request. user)
    shop = Shop.objects.get(id = shop_id)
    if shop.owner != user_prof:
        data = JSONParser().parse(request)
        msg = saveRequest(user_prof,shop_id,data['expected_going_time'],data['expected_leaving_time'])
        return JsonResponse({'msg':msg},safe = False)
    else:
        return JsonResponse({'msg':'Why you are trying to place requests to your own shop'},safe = False)  

@api_view(['GET'],)
@permission_classes([IsAuthenticated])
def seeallShops(request):
    user_prof = UserProfile.objects.get(user = request.user)
    if checkShopkeeper(user_prof):
        shops = Shop.objects.filter(owner = user_prof)
        serializer = ShopSerializer(shops,many = True)
        return JsonResponse(serializer.data,safe = False)
    return JsonResponse({'msg':'you are not a shopkeeper'},safe = False)    



@api_view(['GET'],)    #To see all the requests have been placed to a particular shop
@permission_classes([IsAuthenticated])
def seeallRequests(request,shop_id):
    user_prof = UserProfile.objects.get(user = request.user)
    if checkShopkeeper(user_prof):
        shop = Shop.objects.get(id = shop_id)
        if shop.owner == user_prof:
            re = Request.objects.filter(shop_name = shop)
            serializer = RequestSerializer(re,many = True) #Returns Empty array if any requests have not been placed yet in this shop
            return JsonResponse(serializer.data,safe = False)
        else:
            return JsonResponse({'msg':'You are not the owner of this particular shop'},safe = False)    
    return JsonResponse({'msg':'You are not a shopkeeper'},safe = False)    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_or_decline(request,shop_id,request_id):
    user_prof = UserProfile.objects.get(user=request.user)
    if checkShopkeeper(user_prof):
        shop = Shop.objects.get(id = shop_id)
        re = Request.objects.get(id = request_id)
        if re.shop_name == shop:
            placer = re.placer
            data = JSONParser().parse(request)
            status = True if data['status'] == 'accepted' else False
            no = Notifiaction.objects.create(user_prof = placer,status = status,message = data['message'])    
            re.delete()
            response_data = {
                'msg':data['status']
            }
            return JsonResponse(response_data,safe = False)
        return JsonResponse({'msg':'You are trying to access a shop which is not yours'},safe = False)
    return JsonResponse({'msg':'You are not a shopkeeper'},safe = False)        
    
@api_view(['GET'],)
@permission_classes([IsAuthenticated])
def view_users_request(request):  #All the request that are available for a particular user
    user_prof = UserProfile.objects.get(user=request.user) 
    re = Request.objects.filter(placer = user_prof)
    serializer = RequestSerializer(re,many = True)
    return JsonResponse(serializer.data,safe = False)

@api_view(['GET'],)
@permission_classes([IsAuthenticated])
def view_user_notifications(request): #All the notifications available for a particular user
    user_prof = UserProfile.objects.get(user=request.user)
    no = Notifiaction.objects.filter(user_prof = user_prof)
    serializer = NotificationSerializer(no,many = True)
    return JsonResponse(serializer.data,safe = False)

@api_view(['DELETE'],)
@permission_classes([IsAuthenticated])
def delete_users_requests(request,request_id):
    user_prof = UserProfile.objects.get(user=request.user)
    re = Request.objects.get(id = request_id)
    if re.placer == user_prof:
        re.delete()
        return JsonResponse({'msg':'request Deleted'},safe = False)
    return JsonResponse({'msg':'You should try to delete your own request'},safe = False)

@api_view(['DELETE'],)
@permission_classes([IsAuthenticated])
def delete_users_notifications(request,notification_id):
    user_prof = UserProfile.objects.get(user=request.user)
    no = Notifiaction.objects.get(id = notification_id)
    if no.user_prof == user_prof:
        no.delete()
        return JsonResponse({'msg':'Notification Deleted'}, safe=False)
    return JsonResponse({'msg':'You should try to delete your own request'}, safe=False)

@api_view(['PUT'],)
@permission_classes([IsAuthenticated])
def updateshop(request,shop_id):
    user_prof = UserProfile.objects.get(user=request.user)
    shop = Shop.objects.get(id = shop_id)
    if shop.owner == user_prof:
        data = JSONParser().parse(request)
        msg = updatechanges(data['opening_time'],data['closing_time'],shop)
        if msg is None:
            return JsonResponse({'msg':shop_id},safe = False)
        return JsonResponse(msg,safe = False)
    return JsonResponse({'msg':'You do not have permissions to do this'},safe = False)    



