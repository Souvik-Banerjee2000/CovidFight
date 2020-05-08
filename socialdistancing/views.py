from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import Shop,Request,Notifiaction
from .decoraters import isShopkeeper
from usermanagement.decoraters import unauthenticated_user
from usermanagement.models import UserProfile
from django.contrib import messages
from .utils import save,updatechanges,saveRequest,refractorHour,refractorMinute
from django.contrib.auth.decorators import login_required
import datetime
from django.utils.datastructures import MultiValueDictKeyError
# Create your views here.

def allshops(request):
    shops = Shop.objects.all()
    context = {"shops":shops}
    return render(request,'socialdistancing/home.html',context)
def searchbyLocation(request):
    search = request.POST['search']
    shops = Shop.objects.filter(location__icontains = search)
    context = {
        'shops' : shops,
    }
    return render(request,'socialdistancing/search.html',context)


def searchbyType(request):
    try:
        search = request.POST['search']
    except MultiValueDictKeyError:
        return render(request, 'socialdistancing/search.html')
    shops = Shop.objects.filter(shop_type__icontains=search)
    context = {
        'shops': shops,
    }
    return render(request, 'socialdistancing/search.html', context)



@isShopkeeper
def createshop(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            shop_name = request.POST['shop_name']
            location = request.POST['location']
            shop_type = request.POST['shop_type']
            closing_time = request.POST['closing_time']
            opening_time = request.POST['opening_time']
            save(request,opening_time,closing_time,location,shop_name,shop_type)
            return redirect('/socialdistancing')
        else: 
            return render(request,'socialdistancing/shop.html',context={'flag':True})
    else:
        messages.error(request, 'Login With your Shopkeeper Account First')
        return redirect('/socialdistancing')



@isShopkeeper
def updateshop(request):
    user = request.user
    user_prof = UserProfile.objects.get(user = user)
    shops = Shop.objects.filter(owner = user_prof)
    # print(shops)
    return render(request,'socialdistancing/currentshops.html',context= {'shops':shops})


    

@isShopkeeper
def changeshopdetails(request,id):
    if request.method == 'POST':
        opening_time = request.POST['opening_time']
        closing_time = request.POST['closing_time']
        updatechanges(request,opening_time,closing_time,id)
        return redirect('/socialdistancing')
    else:    
        shop = Shop.objects.get(id = id)
        user_prof = UserProfile.objects.get(user = request.user)
        if shop.owner.user.username == user_prof.user.username:
            return render(request,'socialdistancing/shop.html',context={'flag':False})
        else:
            messages.error(request,'You Are Trying to change other\'s shop you are not allowed to do that')
            return redirect('/socialdistancing')    
@login_required            
def placeRequest(request,id):
    if request.method =='POST':
        shop = Shop.objects.get(id = id)
        expected_going_time = request.POST['expected_going_time']
        expected_leaving_time = request.POST['expected_leaving_time']
        if saveRequest(request,id,expected_going_time,expected_leaving_time):
            if shop.owner.user.id == request.user.id:
                messages.error(request,'Order Placed To your Own shop') 
                return redirect('/socialdistancing')
            else:    
                messages.success(request,'Request Placed Successfully')
                return redirect('/socialdistancing')
        else:
            return redirect('/socialdistancing')

        # return HttpResponseRedirect(reverse('usertype', args=(user_id,)))
    return render(request,'socialdistancing/placerequest.html')    

        
@isShopkeeper
# To see all the requests have been placed to a particular shop
def seeallRequests(request, id):

    user_prof = UserProfile.objects.get(user = request.user)
    shop = Shop.objects.get(owner = user_prof)
    re = Request.objects.filter(shop_name = shop)
    context = {
        'requests':re,
    }
    return render(request,'socialdistancing/allrequests.html',context)

@login_required
@isShopkeeper
def accept_or_decline(request, id, pk):
    if request.method =="POST":
        re = Request.objects.get(pk = pk)
        user = re.placer
        # print(str(user))
        accept_or_declined = request.POST['accept_or_declined']
        message = request.POST['message']
        status = True if accept_or_declined == 'accepted' else False
        Notifiaction.objects.create(user_prof = user,status = status,message = message)
        re.delete()
        return redirect('/socialdistancing')


@login_required
def view_users_requests(request):
    user = request.user
    user_prof = UserProfile.objects.get(user=user)
    requests = Request.objects.filter(placer=user_prof)
    print(requests)
    context = {
        'requests': requests
    }
    return render(request, 'socialdistancing/requests.html', context)

@login_required
def notifications(request):
    user = request.user
    user_prof = UserProfile.objects.get(user = user)
    notifications = Notifiaction.objects.filter(user_prof = user_prof)
    context = {
        'notifications':notifications,
    }
    return render(request,'socialdistancing/notifications.html',context)

@login_required
def delete_users_requests(request,id):
    re = Request.objects.get(id = id)
    if re.placer.user == request.user:
        re.delete()
        return redirect('/socialdistancing')
    else:
        messages.error(request,'You should try to delete your own request' )   
        return redirect('/socialdistancing')


@login_required
def delete_notifications(request,id):
    no = Notifiaction.objects.get(id = id)
    if no.user_prof.user == request.user:
        no.delete()
        return redirect('/socialdistancing')
    else:
        messages.error(request, 'You should try to delete your own Notification')
        return redirect('/socialdistancing')
