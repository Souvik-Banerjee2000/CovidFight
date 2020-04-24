from django.shortcuts import render,redirect
from .models import UserProfile
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .decoraters import unauthenticated_user
# Create your views here.



def home(request):
    return render(request,'usermanagement/index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username = username).exists():
            messages.info(request, 'Usename Taken')
        elif User.objects.filter(email = email).exists():
            messages.info('Email Already in use Try choosing a Different one')  
        else:
            user = User(username = username,password = password,email = email)
            user.set_password(request.POST['password'])
            user.save()
            auth.login(request,user)
            user_id = user.id
            return HttpResponseRedirect(reverse('usertype', args=(user_id,)))
    if request.user.is_authenticated:
        return redirect('/')        
    return render(request,'usermanagement/signuporlogin.html',context = {'flag':True})          

def usertype(request,id):
    if request.method == "POST":
        user_type = request.POST['user_type']
        user = User.objects.get(id = id)
        user_prof = UserProfile(user = user,user_type = user_type)
        user_prof.save()
        return redirect('/')
    else:
        if request.user.is_authenticated:
            user_id = int(id)
            print(user_id)
            user = User.objects.get(id = user_id)
            try:
                user_prof = UserProfile.objects.get(user = user)
                context = {
                    'user_prof':user_prof,
                }
            except ObjectDoesNotExist:
                context = {'user_prof':'create_first'}
    return render(request,'usermanagement/usertype.html',context)    
    

@unauthenticated_user
def login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username,password = password)
        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request,message = 'Invalid credentials')
    return render(request, 'usermanagement/signuporlogin.html',context = {'flag':False})

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')
    else:
        messages.info('Login First')    
